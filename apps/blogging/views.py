from datetime import datetime
import re

from django.db.models import Q
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.template import loader
from django.template.context import RequestContext

from photologue.models import Gallery, Photo

from tf.util import common_data, render, handle_403, data_for_selected_blog
from .models import Blog, Article, Tag


ARCHIVE_LIMIT = 20
GALLERY_MATCHER = re.compile(r'<gallery\s+slug="(?P<gallery_slug>[^"]+)"\s*(/>|>(?P<caption>.*)</gallery>)',
                              re.IGNORECASE | re.MULTILINE)
PHOTO_MATCHER = re.compile(r'<photo\s+slug="(?P<photo_slug>[^"]+)"(\ssize="(?P<size>[^"]+)")?\s*(/>|>(?P<caption>.*)</photo>)',
                            re.IGNORECASE | re.MULTILINE)
YOUTUBE_MATCHER = re.compile(r'<youtube\s+id="(?P<youtube_id>[^"]+)"\s*/>',
                              re.IGNORECASE | re.MULTILINE)


def archive_all(request, selected_tags = None, year = None, month = None, day = None):
    """Display an archive / a search over all blogs."""
    articles = Article.objects.select_related()
    return archive_general(request, "meta_archive_all.html", selected_tags,
                            year, month, day, articles)


def archive(request, author, selected_tags = None, year = None, month = None, day = None):
    """Display an archive / a search over a specific blog."""
    selected_user = User.objects.get(username = author)
    selected_blog = get_object_or_404(Blog, owner__id = selected_user.id)
    articles = Article.objects.select_related().filter(author__id = selected_user.id)
    return archive_general(request, "blog_archive.html", selected_tags,
                            year, month, day, articles,
                            selected_blog = selected_blog,
                            selected_user = selected_user)


def archive_general(request, template, selected_tags, year, month, day, articles,
                     selected_blog = None, selected_user = None):
    """A generic archive view, used by the other, more specialized archive views."""
    search_term = None
    tag_objects = None
    date_selected = None
    date_configuration = {'year': False, 'month': False, 'day': False}
    if "query" in request.GET:
        search_term = request.GET["query"]
        search_query = \
           Q(title__contains = search_term) | Q(html_teaser__contains = search_term) | Q(html__contains = search_term)
        articles = articles.filter(search_query)

    if selected_tags is not None:
        tag_objects = Tag.objects.all().filter(url_name__in = selected_tags.split(","))
        articles = articles.filter(tags__in = tag_objects).distinct()

    if year is not None:
        articles = articles.filter(publication_date__year = int(year))
        date_selected = datetime(int(year), 1, 1)
        date_configuration['year'] = True
        if month is not None:
            articles = articles.filter(publication_date__month = Article.month_number(month))
            date_selected = date_selected.replace(month = Article.month_number(month))
            date_configuration['month'] = True
            if day is not None:
                articles = articles.filter(publication_date__day = int(day))
                date_selected = date_selected.replace(day = int(day))
                date_configuration['day'] = True

    articles = articles.filter(public = True)

    articles = articles[: ARCHIVE_LIMIT]

    archive_user_id = None
    archive_qualifier = ""
    if selected_user is not None:
        archive_user_id = selected_user.id
        archive_qualifier = "/%s" % selected_user.username
        recent_active_months = selected_blog.last_active_months()
    else:
        recent_active_months = Blog.recent_active_months()

    data = common_data(request)
    data.update({"articles": articles,
                 "active_blog": selected_blog,
                 "tags": Tag.used_tags(archive_user_id),
                 "recent_active_months" : recent_active_months,
                 "archive_qualifier": archive_qualifier,
                 "search_term": search_term,
                 "tags_selected": tag_objects,
                 "date_selected": date_selected,
                 "date_configuration": date_configuration})
    return render(template, request, data)


def article(request, author, year, month, day, slug):
    """
    Display a single blog article in its blog.

    If the article references photos or galleries, these references are expanded
    to combinations of previews and links.
    """

    user = User.objects.get(username = author)
    blog = get_object_or_404(Blog, owner__username = author)
    article = get_object_or_404(Article,
                                author__id = user.id,
                                publication_date__year = int(year),
                                publication_date__month = Article.month_number(month),
                                publication_date__day = int(day),
                                title_in_url = slug)

    if not (article.public or request.user.is_authenticated()):
        return handle_403(request)

    older_articles = Article.objects.filter(publication_date__lt = article.publication_date,
                                             author = user).order_by("-publication_date")
    newer_articles = Article.objects.filter(publication_date__gt = article.publication_date,
                                             author = user).order_by("publication_date")

    if not request.user.is_authenticated():
        older_articles = older_articles.filter(public = True)
        newer_articles = newer_articles.filter(public = True)

    try: previous_article = older_articles[0]
    except IndexError: previous_article = None

    try: next_article = newer_articles[0]
    except IndexError: next_article = None

    data = common_data(request)
    data.update({"article": article,
                 "previous_article": previous_article,
                 "next_article": next_article,
                 "active_blog": blog,
                 "tags": Tag.used_tags(user.id),
                 "recent_active_months" : blog.last_active_months(),
                 "archive_qualifier": "/%s" % user.username})

    # Substitute gallery links:
    def gallery_link(match):
        gallery = get_object_or_404(Gallery, title_slug = match.group("gallery_slug"))
        context = RequestContext(request, dict = {"gallery": gallery,
                                                  "caption": match.group("caption") or gallery.description})
        return loader.render_to_string("gallery_fragment.html", None, context)

    data["html_teaser"] = GALLERY_MATCHER.sub(gallery_link, data["article"].html_teaser)
    data["html_text"] = GALLERY_MATCHER.sub(gallery_link, data["article"].html)

    # Substitute photo links:
    def photo_link(match):
        photo = get_object_or_404(Photo, title_slug = match.group("photo_slug"))
        size = match.group("size") or "display"
        url = photo.__getattribute__("get_standalone_%s_url" % size)()
        context = RequestContext(request, dict = {"photo": photo,
                                                  "url": url,
                                                  "size": size,
                                                  "caption": match.group("caption") or photo.caption})
        return loader.render_to_string("photo_fragment.html", None, context)

    data["html_teaser"] = PHOTO_MATCHER.sub(photo_link, data["html_teaser"])
    data["html_text"] = PHOTO_MATCHER.sub(photo_link, data["html_text"])

    # Substitute youtube links:
    def youtube_link(match):
        youtube_id = match.group("youtube_id")
        context = RequestContext(request, dict = {"youtube_id": youtube_id})
        return loader.render_to_string("youtube_fragment.html", None, context)

    data["html_teaser"] = YOUTUBE_MATCHER.sub(youtube_link, data["html_teaser"])
    data["html_text"] = YOUTUBE_MATCHER.sub(youtube_link, data["html_text"])

    return render("blog_article.html", request, data)


def about(request, author):
   user = User.objects.get( username = author )
   return render("blog_about.html", request, data_for_selected_blog(request, user))

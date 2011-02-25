from datetime import date

from django.conf import settings
from django.utils import feedgenerator
from django.http import HttpResponse

from .models import Article


def feed(request, author = None, selected_tags = None):
    articles = Article.objects.filter(public = True).select_related()
    if (author is not None):
        articles = articles.filter(author__username = author)
    if (selected_tags is not None):
        tags = selected_tags.split(",")
        articles = articles.filter(tags__url_name__in = tags)

    feed = feedgenerator.Atom1Feed(
        "thefoundation",
        settings.HOST_NAME,
        "Birds of a feather and a flock.",
        feed_url = "%s/feeds/everything" % settings.HOST_NAME,
        language = "en-US",
        feed_copyright = "(c) %d Michael Kurze, Aachen, Germany" %
                         (date.today().year)
    )
    articles = articles.order_by("-publication_date")[: settings.FEED_LIMIT]

    for article in articles:
        feed.add_item(title=article.title,
                      link="http://%s%s" % (request.META['host_name'],
                                            article.get_absolute_url()),
                      unique_id=article.title_in_url,
                      description="<p>%s</p>%s" % (article.html_teaser,
                                                     article.html),
                      subtitle=article.html_teaser,
                      author_name="%s %s" % (article.author.first_name,
                                               article.author.last_name),
                      author_link="%s/about/%s" % (settings.HOST_NAME,
                                                     article.author.username),
                      pubdate=article.publication_date)

    return HttpResponse(feed.writeString("utf-8"))

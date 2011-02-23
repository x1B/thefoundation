""" theFoundation blogging and tagging models
"""

from datetime import datetime, date

from django.db import models, connection
from django.contrib.auth.models import User
from django.conf import settings

from middleware import current_user


def fetch_dicts(query_string, *query_args):
    """Run a simple query and produce a generator that returns a dict
    for each row, with keys for the selected column names.
    """
    cursor = connection.cursor()
    cursor.execute(query_string, query_args)
    col_names = [desc[0] for desc in cursor.description]
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        row_dict = dict(izip(col_names, row))
        yield row_dict
    return


def fetch_rows(query_string, *query_args):
    """Run a simple query and produce a generator
    that returns the results as a bunch of tupels.
    """
    cursor = connection.cursor()
    cursor.execute(query_string, query_args)
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        yield row
    return


# :KEYWORD: SQL-BRANCH
month_expression_ = {}
month_expression_["postgresql_psycopg2"] = "to_char(publication_date, 'YYYY-MM')"
month_expression_["sqlite3"] = 'strftime("%%Y-%%m", publication_date)'

class Blog(models.Model):
    """A collection of articles, owned by an Author."""
    owner = models.ForeignKey(User)
    title = models.CharField(max_length = 200)
    sub_title = models.CharField(max_length = 200)
    html_resume_teaser = models.TextField("html resume teaser", db_index = True)
    html_resume = models.TextField("html resume", db_index = True)

    @staticmethod
    def recent_active_months():
        return list(Article.objects.filter(public = True)
                     .dates("publication_date", "month", order = "DESC").distinct())

    month_count_ = None
    def month_count(self):
        if self.month_count_ is not None: return self.month_count_
        self.month_count_ = dict([(row[1], row[0]) for row in
                                  fetch_rows('''SELECT COUNT(*) as c, '''
                                              + month_expression_[settings.DATABASE_ENGINE] + ''' AS month
                                                FROM blogging_article AS a
                                                WHERE a.author_id = %s AND a.public
                                                GROUP BY month;''',
                                                self.owner.id)])
        return self.month_count_

    last_active_months_ = None
    def last_active_months(self):
        if self.last_active_months_ is not None: return self.last_active_months_
        self.last_active_months_ = list(Article.objects.filter(author = self.owner, public = True)
                                                        .dates("publication_date", "month", order = "DESC")
                                                        .distinct())
        return self.last_active_months_

    def __unicode__(self):
        return self.owner.username + "s blog \"" + self.title + "\""

    tags_ = None
    def tags(self):
        if self.tags_ is not None: return self.tags_
        self.tags_ = Tag.used_tags(self.owner_id)
        return self.tags_

    def get_absolute_url(self):
        return "/%s/" % self.owner.username

    class Meta:
        ordering = ["owner__date_joined"]



class Tag(models.Model):
    name = models.CharField(max_length = 40, unique = True, db_index = True)

    url_name = models.SlugField("tag in URLs",
                                max_length = 50,
                                unique = True,
                                db_index = True)

    @staticmethod
    def used_tags(by_userid = None):
        """Return a list of tags that are used in any article (of the given author)."""
        if by_userid is None:
            results = Tag.objects.extra(
               select = {
                  "article_count":
                     """SELECT COUNT(*)
                        FROM blogging_article_tags AS tba LEFT JOIN blogging_article AS a
                        ON tba.article_id = a.id
                        WHERE tba.tag_id = blogging_tag.id
                        AND a.public"""})
        else:
            results = Tag.objects.extra(
               select = {
                  "article_count":
                     """SELECT COUNT(*)
                        FROM blogging_article_tags AS tba LEFT JOIN blogging_article AS a
                        ON tba.article_id = a.id
                        WHERE tba.tag_id = blogging_tag.id
                        AND a.author_id = %s
                        AND a.public"""},
               select_params = [by_userid])

        return [tag for tag in results if tag.article_count > 0]

    def __unicode__(self):
        return self.name



class Article(models.Model):
    """An article in a blog."""
    MONTHS = ("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec")
    MONTH_NUMBERS = dict(zip(MONTHS, range(1, 12+1)))

    @staticmethod
    def month_name(number):
        """Name for number from 1 to 12."""
        return Article.MONTHS[number - 1]

    @staticmethod
    def month_number(name):
        """Number from 1 to 12 for name form "jan" to "dec"."""
        return Article.MONTH_NUMBERS[name]

    author           = models.ForeignKey(User,
                                         related_name = "articles",
                                         editable = False)
    title            = models.CharField("title",
                                        max_length = 110,
                                        db_index = True,
                                        unique_for_date = "publication_date")
    title_in_url     = models.SlugField("title in URL",
                                        db_index = True,
                                        max_length = 60,
                                        unique = True,
                                        unique_for_date = "publication_date")
    html_teaser      = models.TextField("html teaser", db_index = True)
    html             = models.TextField("html article", db_index = False)
    public           = models.BooleanField("public", default = False)
    was_published    = models.BooleanField("Published", editable = False, default = False)
    modified         = models.DateTimeField("last modified", editable = False, auto_now = True)
    publication_date = models.DateTimeField("Created / Published", editable = False, auto_now_add = True)
    tags             = models.ManyToManyField(Tag,
                                              related_name = "articles",
                                              blank = True)

    def get_absolute_url(self):
        return "/%s/%04d/%s/%02d/%s/" % (self.author.username, self.publication_date.year,
                                          Article.month_name(self.publication_date.month),
                                          self.publication_date.day, self.title_in_url)


    def save(self):
        if self.author_id is None:
            self.author_id = current_user.current_user().id
        elif self.author_id != current_user.current_user().id:
            # Cannot override an article of another author.
            raise Exception("Permission denied. This article belongs to %s."
                             % User.objects.get(id = self.author_id).first_name)
        if self.public and not self.was_published:
            self.was_published = True
            self.publication_date = datetime.today()
        super(Article, self).save()

    def author_name(self):
        return self.author.first_name + " " + self.author.last_name
    author_name.short_description = "Author"

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["-publication_date"]



class Comment(models.Model):
    """A comment on an article."""
    pass
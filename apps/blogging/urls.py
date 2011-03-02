from django.conf.urls.defaults import patterns, url


yyyy = r'(?P<year>\d{4})/'
yyyy_mmm = r'%s(?P<month>[a-z]{3})/' % (yyyy, )
yyyy_mmm_dd = r'%s(?P<day>\d{2})/' % (yyyy_mmm, )
item = r'(?P<slug>[a-zA-Z0-9_-]+)/'

author = r'(?P<author>daniel|david|matthias|michael)/'
tags = r'(on/(?P<selected_tags>[a-zA-Z][a-zA-Z0-9_,-]*)/)?'


urlpatterns = patterns(
    'blogging.views',

    # an individual blog article
    url(r'^%s%s%s$' % (author, yyyy_mmm_dd, item), 'article'),

    # aggregate blog archives and search through all blogs
    url(r'^%s$' % tags, 'archive_all'),
    url(r'^%s%s/$' % (tags, yyyy), 'archive_all'),
    url(r'^%s%s$' % (tags, yyyy_mmm), 'archive_all'),
    url(r'^%s%s$', 'archive_all'),

    # blog archives and search for a single author
    url(r'^%s%s$' % (author, tags), 'archive'),
    url(r'^%s%s%s$' % (author, tags, yyyy), 'archive'),
    url(r'^%s%s%s$' % (author, tags, yyyy_mmm), 'archive'),
    url(r'^%s%s%s$' % (author, tags, yyyy_mmm_dd), 'archive'),

    url(r'^about/%s$' % (author, ), 'about'),

    url(r'^search/$', 'archive_all'),
    url(r'^%s%ssearch/$' % (author, tags), 'archive'),
)


urlpatterns += patterns(
    'blogging.views_feeds',

    url(r'^feeds/everything/$', 'feed'),
    url(r'^feeds/%s$' % tags, 'feed'),
    url(r'^feeds/%s%s$' % (author, tags), 'feed'),
)

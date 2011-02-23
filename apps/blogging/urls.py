from django.conf.urls.defaults import patterns, url
import views

# General
yyyy = r'(?P<year>\d{4})/'
yyyy_mmm = r'%(yyyy)s(?P<month>[a-z]{3})/' % (year, )
yyyy_mmm_dd = r'%(yyyy_mmm)s(?P<day>\d{2})/' % (month, )
item = r'%(yyyy_mmm_dd)s(?P<slug>[a-zA-Z0-9_-]+)/'

# Blogging
author = r'(?P<author>daniel|david|matthias|michael)/'
tags = r'(on/(?P<selected_tags>[a-zA-Z][a-zA-Z0-9_,-]*)/)?'

# galleries
galleryPattern =
    r'^gallery/(?P<gallery_slug>[a-zA-Z0-9_-]+)/"' \
    r'((?P<image_slug>[a-zA-Z0-9_-]+))?$'
imagePattern = r'^photo/(?P<image_slug>[a-zA-Z0-9_-])/'

urlpatterns = patterns('blogging.views',
    # site overview / homepage
    url(r'^$', 'start'),

    # an individual blog article
    url(r'^%(author)s%(item)s$' % (author, item), 'article'),

    # various blog archives and search for articles of a single author
    url(r'^%(author)s%(tags)s$' % (author, tag), 'archive'),
    url(r'^%(author)s%(tags)s%(year)s$' % (author, tag, year), 'archive'),
    url(authorExp + tagExp + monthExp + r'$' % (author, tag, month), 'archive'),
    url(authorExp + tagExp + dateExp  + r'$' % (author, tag, date), 'archive'),
    url(authorExp + r'search/$' % (author, tag), 'archive'),

    # aggregate blog archives and search for all authors
    url(r'^%(tag)s$' % tagExp, 'archive_all'),
    url(r'^%(tag)s%(year)s/$' % (tagExp, yearExp), 'archive_all'),
    url(r'^%(tag)s%(month)s$' % (tagExp, monthExp), 'archive_all'),
    url(r'^%(tag)s%(date)s$', 'archive_all'),

    # search (all)
    url(r'search/$', 'archive_all'),

    # about pages
    url(r'about/' + authorExp + r'$', views.about),
    url(r'about/$', views.about),
    url(r'imprint/$', views.imprint),
    url(r'contact/$', views.contact),

    # login form action
    url(r'login/$', views_management.login),
    url(r'login/submit/$', views_management.login_submit),
    url(r'login/failed/$', views_management.login_failed),
    url(r'logout/$', views_management.logout),

    url(r'feeds/everything/$', views_feeds.feed),
    url(r'feeds/%s$' % tagExp, views_feeds.feed),
    url(r'feeds/%s/%s$' % (authorExp, tagExp), views_feeds.feed),

    # management
    url(managementPrefix + r'$', blogging.views_management.manage),

)


# galleries
urlpatterns += patterns('blogging.views_gallery',
   url( r'^galleries/$',                 blogging.views_gallery.galleries),
   url( galleryPattern, 'gallery'),
   url( imagePattern + r'$',             blogging.views_gallery.photo),
   url( imagePattern + r'description/$', blogging.views_gallery.photo_description),
),
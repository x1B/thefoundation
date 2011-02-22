import re

from django.conf.urls.defaults import include, patterns, url

from django.conf.urls.defaults import *
from django.contrib import admin

from thefoundation import blogging
from django.conf import settings

import blogging.views
import blogging.views_feeds
import blogging.views_management
import blogging.views_gallery
import thefoundation.external.photologue
import thefoundation.external.photologue.urls

# Admin Site
admin.autodiscover()


# General
yearExp   = r'(?P<year>\d{4})/'
monthExp  = yearExp + r'(?P<month>[a-z]{3})/'
dateExp   = monthExp + r'(?P<day>\d{2})/'
objectExp = dateExp + r'(?P<slug>[a-zA-Z0-9_-]+)/'

# Blogging
bloggingPrefix = r'^'
authorExp = r'(?P<author>daniel|david|matthias|michael)/'
tagExp    = r'(on/(?P<selected_tags>[a-zA-Z][a-zA-Z0-9_,-]*)/)?'

# Blogging + RSS
rssPrefix = r'feeds/'


# Management
managementPrefix = r'^manage/'

handler403 = "thefoundation.blogging.view_helpers.handle_403"
handler404 = "thefoundation.blogging.view_helpers.handle_404"
handler405 = "thefoundation.blogging.view_helpers.handle_405"
handler500 = "thefoundation.blogging.view_helpers.handle_500"

urlpatterns = patterns( '',
   
   ###  Blogging  ############################################################################################
   
   # site overview / homepage
   url( bloggingPrefix + r'$',                                 blogging.views.start ),

   # an individual blog article
   url( bloggingPrefix + authorExp + objectExp + r'$' ,        blogging.views.article ),

   # various blog archives and search for articles of a single author
   url( bloggingPrefix + authorExp + tagExp + r'$',            blogging.views.archive ),
   url( bloggingPrefix + authorExp + tagExp + yearExp  + r'$', blogging.views.archive ),
   url( bloggingPrefix + authorExp + tagExp + monthExp + r'$', blogging.views.archive ),
   url( bloggingPrefix + authorExp + tagExp + dateExp  + r'$', blogging.views.archive ),
   url( bloggingPrefix + authorExp + r'search/$',              blogging.views.archive ),

   # aggregate blog archives and search for all authors
   url( bloggingPrefix + tagExp + r'$',                        blogging.views.archive_all ),
   url( bloggingPrefix + tagExp + yearExp + r'$',              blogging.views.archive_all ),
   url( bloggingPrefix + tagExp + monthExp + r'$',             blogging.views.archive_all ),
   url( bloggingPrefix + tagExp + dateExp + r'$',              blogging.views.archive_all ),
   url( bloggingPrefix + r'search/$',                          blogging.views.archive_all ),

   # about pages
   url( bloggingPrefix + r'about/' + authorExp + r'$',         blogging.views.about ),
   url( bloggingPrefix + r'about/$',                           blogging.views.about ),
   url( bloggingPrefix + r'imprint/$',                         blogging.views.imprint ),
   url( bloggingPrefix + r'contact/$',                         blogging.views.contact ),
   
   # login form action
   url( bloggingPrefix + r'login/$',                           blogging.views_management.login ),
   url( bloggingPrefix + r'login/submit/$',                    blogging.views_management.login_submit ),
   url( bloggingPrefix + r'login/failed/$',                    blogging.views_management.login_failed ),
   url( bloggingPrefix + r'logout/$',                          blogging.views_management.logout ),
   
   # management
   url( managementPrefix + r'$',                               blogging.views_management.manage ),


   ###  Blogging/RSS  ########################################################################################
   
   url( rssPrefix + r'everything/$',                           blogging.views_feeds.feed ),
   url( rssPrefix + tagExp + r'$',                             blogging.views_feeds.feed ),
   url( rssPrefix + authorExp + tagExp + r'$',                 blogging.views_feeds.feed ), 


   ###  Admin  ###############################################################################################

   # admin URLs:
   url( r'^admin/(.*)',                                        admin.site.root ),
)



###  Photologue Galleries ####################################################################################

galleryPrefix = r'^'
galleryPattern = galleryPrefix + r'gallery/(?P<gallery_slug>[a-zA-Z0-9_-]+)/((?P<image_slug>[a-zA-Z0-9_-]+))?$'
imagePattern = galleryPrefix + r'photo/(?P<image_slug>[a-zA-Z0-9_-])/'

urlpatterns += patterns( '',
   url( r'^galleries/$',                 blogging.views_gallery.galleries ),
   url( galleryPattern,                  blogging.views_gallery.gallery ),
   url( imagePattern + r'$',             blogging.views_gallery.photo ),
   url( imagePattern + r'description/$', blogging.views_gallery.photo_description ),
)

# Include photologue predefined URLs. These are intended for the photologue admin pages to work.
# :TODO: Make these pages more pretty / useful.
urlpatterns += patterns( '', ( galleryPrefix, include( "thefoundation.external.photologue.urls" ) ), )


if settings.DEBUG:
    ### static files for development ########################################################################
    urlpatterns += patterns( '',
        ( r'^(?P<path>favicon.ico)$', 'django.views.static.serve', { 'document_root': '%s/_root_' % settings.MEDIA_ROOT, 
                                                                     'show_indexes': True } ),
        ( r'^(?P<path>robots.txt)$', 'django.views.static.serve', { 'document_root': '%s/_root_' % settings.MEDIA_ROOT, 
                                                                    'show_indexes': True } ),
        ( r'^media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT, 
                                                                  'show_indexes': True } ),
    )
else:
    ### memcached ###########################################################################################
    urlpatterns += patterns( '',
        ( r'^status/cache/$', 'thefoundation.external.memcached_status.view' ),
    )


    

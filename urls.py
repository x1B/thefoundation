import re

from django.conf.urls.defaults import include, patterns, url

from django.conf.urls.defaults import *
from django.contrib import admin

from django.conf import settings

import thefoundation.external.photologue
import thefoundation.external.photologue.urls

# Admin Site
admin.autodiscover()

# Management
managementPrefix = r'^manage/'

handler403 = "thefoundation.blogging.view_helpers.handle_403"
handler404 = "thefoundation.blogging.view_helpers.handle_404"
handler405 = "thefoundation.blogging.view_helpers.handle_405"
handler500 = "thefoundation.blogging.view_helpers.handle_500"

urlpatterns = patterns( '',
    ('', include('blogging.urls')),
    url( r'^admin/(.*)', admin.site.root),
)


###  Photologue Galleries

# Include photologue predefined URLs. These are intended for the photologue admin pages to work.
# :TODO: Make these pages more pretty / useful.
urlpatterns += patterns( '', ( galleryPrefix, include( "thefoundation.external.photologue.urls" )), )


if settings.DEBUG:
    ### static files for development ########################################################################
    urlpatterns += patterns( '',
        ( r'^(?P<path>favicon.ico)$', 'django.views.static.serve', {'document_root': '%s/_root_' % settings.MEDIA_ROOT,
                                                                     'show_indexes': True}),
        ( r'^(?P<path>robots.txt)$', 'django.views.static.serve', {'document_root': '%s/_root_' % settings.MEDIA_ROOT,
                                                                    'show_indexes': True}),
        ( r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,
                                                                  'show_indexes': True}),
    )

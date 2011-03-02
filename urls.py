from django.conf import settings
from django.conf.urls.defaults import include, patterns
from django.contrib import admin

# Admin Site
admin.autodiscover()

handler403 = "tf.view_helpers.handle_403"
handler404 = "tf.view_helpers.handle_404"
handler405 = "tf.view_helpers.handle_405"
handler500 = "tf.view_helpers.handle_500"

urlpatterns = patterns('',
    ('', include('tf.urls')),
    ('', include('blogging.urls')),
    ('', include('galleries.urls')),
    ('', include('management.urls')),

    (r'^admin/', include(admin.site.urls)),
    (r'^comments/', include('django.contrib.comments.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('django.views',
        (r'^(?P<path>favicon.ico)$', 'static.serve',
         {'document_root': '%s/_root_' % settings.MEDIA_ROOT}),

        (r'^(?P<path>robots.txt)$', 'static.serve',
         {'document_root': '%s/_root_' % settings.MEDIA_ROOT}),

        (r'^media/(?P<path>.*)$', 'static.serve',
         {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )

from django.conf.urls.defaults import patterns, url


urlpatterns = patterns(
    'management.views',

    url(r'^manage/$',       'manage'),

    url(r'^login/$',        'login'),
    url(r'^login/submit/$', 'login_submit'),
    url(r'^login/failed/$', 'login_failed'),
    url(r'^logout/$',       'logout'),
)

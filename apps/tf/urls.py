from django.conf.urls.defaults import patterns, url


urlpatterns = patterns(
    'tf.views',

    # site overview / homepage
    url(r'^$', 'start'),

    # about pages
    url(r'^about/$', 'about'),

    url(r'^imprint/$', 'imprint'),
    url(r'^contact/$', 'contact'),
)

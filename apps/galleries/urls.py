from django.conf.urls.defaults import patterns, url


galleryPattern = r'^gallery/(?P<gallery_slug>[a-zA-Z0-9_-]+)/"' \
                 r'((?P<image_slug>[a-zA-Z0-9_-]+))?$'

photoPattern = r'^photo/(?P<image_slug>[a-zA-Z0-9_-])/'


urlpatterns = patterns(
    'galleries.views',

    url(r'^galleries/$', 'galleries'),
    url(galleryPattern, 'gallery'),
    url(photoPattern + r'$', 'photo'),
    url(photoPattern + r'description/$', 'photo_description'),
)

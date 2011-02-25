from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404

from photologue.models import Gallery, Photo

from tf.util import data_for_all, render, common_data


def galleries(request):
    """Galleries overview"""
    data = data_for_all(request)
    data["galleries"] = Gallery.objects.all()
    return render("meta_manage_galleries.html", request, data)


def gallery(request, gallery_slug, image_slug = None):
    """Display the Gallery Viewer, optionally opened at a specific image."""
    gallery = get_object_or_404(Gallery, title_slug = gallery_slug)
    photos = gallery.photos.filter(is_public = True).order_by("date_taken")[:]

    if len(photos) == 0:
        raise Http404
    if image_slug is None:
        image_slug = photos[0].title_slug

    next, current, prev = None, None, None
    for index, current in enumerate(photos):
        try: next = photos[index + 1]
        except IndexError: next = None
        if current.title_slug == image_slug:
            break
        prev = photos[index]

    if current is None:
        raise Http404

    data = common_data(request)
    data.update({"gallery": gallery, "photos": photos, "prev": prev,
                 "current": current, "next": next})
    return render("photologue/gallery_detail.html", request, data)


def photo_description(request, image_slug):
    """Photo description (used by gallery)."""
    photo = get_object_or_404(Photo, title_slug = image_slug)
    return HttpResponse(photo.caption)

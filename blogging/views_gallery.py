from django.http import Http404, HttpResponse

from thefoundation.external.photologue.models import Gallery, Photo
from django.core.exceptions import ObjectDoesNotExist

from view_helpers import *


def galleries( request ):
   """Galleries overview"""
   data = data_for_all( request )
   data[ "galleries" ] = Gallery.objects.all()
   return render( "meta_manage_galleries.html", request, data )


def gallery( request, gallery_slug, image_slug = None ):
   """Display the Gallery Viewer, optionally opened at a specific image."""
   gallery = get_object_or_404( Gallery, title_slug = gallery_slug )
   photos = gallery.photos.filter( is_public = True ).order_by( "date_taken" )[ : ]

   if len( photos ) == 0: raise Http404
   if image_slug is None: 
      image_slug = photos[ 0 ].title_slug
   # import sys
   next, current, prev = None, None, None
   #sys.stderr.write( "----- looking for %s \n" % image_slug )
   for index, current in enumerate( photos ):
      #sys.stderr.write( "----- checking %s \n" % current.title_slug )
      try: next = photos[ index + 1 ]
      except IndexError: next = None
      if current.title_slug == image_slug:
         break
      prev = photos[ index ]

   if current is None: raise Http404
   
   #sys.stderr.write( "----- Prev: %s ---- Next: %s \n" % (prev, next ) )

   data = common_data( request )
   data.update( { "gallery": gallery, "photos": photos, "prev": prev, "current": current, "next": next } )
   return render( "photologue/gallery_detail.html", request, data )


def photo( request, image_slug ):
   """Display a single image independent of any galleries it might belong to."""
   gallery = get_object_or_404( Photo, title_slug = image_slug )


def photo_description( request, image_slug ):
   """Photo description (used by gallery)."""
   photo = get_object_or_404( Photo, title_slug = image_slug )
   return HttpResponse( photo.caption )

from django.template import loader
from django.template.context import RequestContext
from django.http import *
from django.shortcuts import get_object_or_404

from django.conf import settings
from models import Blog, Article, Tag

#############################################################################################################
# Helper Methods

def render( template, request, dict ):
   """General purpose helper."""
   context = RequestContext( request, dict = dict )
   return HttpResponse( loader.render_to_string( template, None, context ) )

def common_data( request ):
   current_user = None
   if request.user.is_authenticated and request.user.is_active:
      current_user = request.user
   return { "latest_articles":  Article.objects.select_related().filter( public = True )[ : 5 ], 
            "blogs": Blog.objects.select_related(),
            "active_blog": None,
            "login_failed": False,
            "current_user": current_user,
            "debug_js": settings.DEBUG_JS,
            "debug_css": settings.DEBUG_CSS }

def data_for_all( request ):
   """This data is used for all normal pages where no blog is selected."""
   data = common_data( request )
   data.update( { "tags": Tag.used_tags(),
                  "archive_qualifier": "",
                  "recent_active_months" : Blog.recent_active_months() } )
   return data

def data_for_selected_blog( request, user ):
   data = common_data( request )
   active_blog = get_object_or_404( Blog, owner__id = user.id )
   data.update( { "active_blog": active_blog,
                  "tags": Tag.used_tags( user.id ),
                  "archive_qualifier": "/%s" % user.username,
                  "recent_active_months" : active_blog.last_active_months() } )
   return data


#############################################################################################################
# Decorators

def login_required( view ):
   def inner( request, *args, **kwargs ):
      if not request.user.is_authenticated():
          return handle_403( request, *args, **kwargs )
      return view( request, *args, **kwargs )
   return inner

def require_POST( view ):
   def inner( request, *args, **kwargs ):
      if request.method != "POST":
          return handle_405( request, [ "POST" ], **kwargs )
      return view( request, *args, **kwargs )
   return inner


#############################################################################################################
# Context Processors

def login_required_processor( request ):
   """Throw 404 for non unauthenticated clients on anything but login!"""
   if request.user.is_authenticated():
      return { }
   if request.META.has_key( "de.thefoundation.DENIED" ):
      return { }
   if request.path.startswith( u"/media/" ):
      return { }
   if request.path in [ '/login/', '/login/failed/', '/imprint/' ]:
      return { }
   request.META[ "de.thefoundation.DENIED" ] = True
   raise Http404( handle_404( request ) )


#############################################################################################################
# Error handlers

def handle_error( request, response, template ):
   """Display an error page."""
   blogs = Blog.objects.select_related()
   tags = Tag.used_tags()
   recent_active_months = Blog.recent_active_months()
   context = RequestContext( request, 
                             dict = { "blogs": blogs, 
                                      "tags": tags, 
                                      "archive_qualifier": "",
                                      "recent_active_months" : recent_active_months } )
   response.write( loader.render_to_string( template, None, context ) )
   return response

def handle_403( request ):
   """Handle permission denied."""
   return handle_error( request, HttpResponseForbidden(), "403.html" )

def handle_404( request ):
   """Handle resource not found."""
   return handle_error( request, HttpResponseNotFound(), "404.html" )

def handle_405( request, permitted_methods ):
   """Handle method not allowed."""
   return handle_error( request, HttpResponseNotAllowed( permitted_methods ), "405.html" )

def handle_500( request ):
   """Handle internal error."""
   return handle_error( request, HttpResponseServerError(), "500.html" )


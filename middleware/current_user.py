from django.contrib.auth.models import User
import threading

thread_locals = threading.local()

def current_user():
   return thread_locals.user

class ThreadLocals( object ):
   """Middleware that gets various objects from the
   request object and saves them in thread local storage."""
   def process_request( self, request ):
      thread_locals.user = request.user

import logging
import traceback, sys
import os.path
from django.conf import settings
from django import http

from thefoundation.external.exception_helpers import exc_string

logging.basicConfig()

log = logging.FileHandler( settings.LOG_FILE )
log.setFormatter( logging.Formatter('%(asctime)s| %(name)-10s|%(levelname)-5s %(message)s') )

logger = logging.getLogger( "Exceptions" )
logger.setLevel( settings.LOG_LEVEL )
logger.addHandler( log )


class LogExceptionsMiddleware( object ):
   """Log instead of mail in case of errors."""
   
   def process_exception( self, request, exception ):
      if isinstance( exception, http.Http404 ):
         return None # use default 404 handling

      logger.error( "FROM: %s | %s" % ( request.META.get( "REMOTE_ADDR" ), exc_string() ) )
      if logger.isEnabledFor( logging.DEBUG ):
         try: request_repr = repr( request )
         except: request_repr = "[cannot represent request]"
         logger.debug( "REQUEST: %s" % request_repr )

      return None # continue to default error page


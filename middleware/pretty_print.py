from django.conf import settings

import logging

class PrettyPrintMiddleware( object ):
   """
   prettify indention of source html
   """
   def process_response( self, request, response ):
      if not ( response.has_header( 'Content-Type' ) and 
               response['Content-Type'].startswith( 'text/html' ) ):
         return response
      if settings.DEBUG and request.path.startswith( '/media/' ): 
         return response
      
      text = unicode( response.content, settings.DEFAULT_CHARSET )

      def lines( text ):
         line = []
         i = 0
         while i < len( text ):
            line.append( text[ i ] )
            if text[ i ] == '\n': 
               yield line
               line = []
            i += 1
         raise StopIteration()
      
      def startswith( list, bytes ):
         i = 0
         for byte in bytes:
            if list[ i ] != byte: return False
         return True
      
      def delimits_preserve_area( line, position ):
         return startswith( line[ position: ], "textarea" ) or \
                startswith( line[ position: ], "code" ) or \
                startswith( line[ position: ], "pre" )
      
      do_preserve = False
      content = []
      indent = 0
      for line in lines( text ):
         p, length = 0, len( line )
         if not do_preserve:
            # remove previous, ugly indent
            while p < length and ( line[ p ] == ' ' or line[ p ] == '\t' ): p += 1
            # strip line if it consists of whitespace entirely
            if p >= length - 1: continue
            # peek ahead for correct indent of current line
            next = line[ p + 1 ]
            if line[ p ] == '<' and next == '/': indent -= 1
            # print indent and the rest of the line
            content.append( ' ' * indent )
         content.extend( line[ p: ] )
         # update indent for the next line
         if line[ p ] == '<' and next != '/' and next != '!': 
            indent += 1
            logging.info( "NEXT: %s", "".join( line[ p:p+20 ] ).encode( "us-ascii" ) )
            if delimits_preserve_area( line, p+1 ):
               logging.info( "entering preserve" )
               do_preserve = True 
         elif line[ p ] == '/' and next == '>': indent -= 1
         while p < length - 2:
            p += 1
            next = line[ p + 1 ]
            if line[ p ] == '<':
               if next == '/': 
                  if do_preserve and delimits_preserve_area( line, p ):
                        logging.info( "leaving preserve" )
                        do_preserve = False
                  else:
                     indent -= 1
               elif next == '!': pass
               else: 
                  indent += 1
                  if delimits_preserve_area( line, p+1 ):
                     logging.info( "entering preserve: %s", "".join( line[ p:p+20 ] ).encode( "us-ascii" )  )
                     do_preserve = True
            elif line[ p ] == '/' and next == '>': indent -= 1

      # print content
      response.content = ( u"".join( content ) ).encode( settings.DEFAULT_CHARSET )
      return response

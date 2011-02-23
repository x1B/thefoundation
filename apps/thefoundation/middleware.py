import logging, traceback, sys, os.path

from django.conf import settings
from django.conf import settings
from django import http

from django.contrib.auth.models import User
import threading

from exception_helpers import set_exc_string_encoding, exc_string
set_exc_string_encoding("utf-8")


logging.basicConfig()

log = logging.FileHandler(settings.LOG_FILE)
log.setFormatter(logging.Formatter('%(asctime)s| %(name)-10s|%(levelname)-5s %(message)s'))

logger = logging.getLogger("Exceptions")
logger.setLevel(settings.LOG_LEVEL)
logger.addHandler(log)


class LogExceptionsMiddleware(object):
    """Log instead of mail in case of errors."""

    def process_exception(self, request, exception):
        if isinstance(exception, http.Http404): return None

        logger.error("FROM: %s | %s" % (request.META.get("REMOTE_ADDR"), exc_string()))
        if logger.isEnabledFor(logging.DEBUG):
            try: request_repr = repr(request)
            except: request_repr = "[cannot represent request]"
            logger.debug("REQUEST: %s" % request_repr)

        return None # default error page


class PrettyPrintMiddleware(object):
    """prettify indention of source html
    """
    def process_response(self, request, response):
        if not (response.has_header('Content-Type') and
                 response['Content-Type'].startswith('text/html')):
            return response
        if settings.DEBUG and request.path.startswith('/media/'):
            return response

        text = unicode(response.content, settings.DEFAULT_CHARSET)

        def lines(text):
            line = []
            i = 0
            while i < len(text):
                line.append(text[i])
                if text[i] == '\n':
                    yield line
                    line = []
                i += 1
            raise StopIteration()

        def startswith(list, bytes):
            i = 0
            for byte in bytes:
                if list[i] != byte: return False
            return True

        def delimits_preserve_area(line, position):
            return startswith(line[position:], "textarea") or \
                   startswith(line[position:], "code") or \
                   startswith(line[position:], "pre")

        do_preserve = False
        content = []
        indent = 0
        for line in lines(text):
            p, length = 0, len(line)
            if not do_preserve:
                # remove previous, ugly indent
                while p < length and (line[p] == ' ' or line[p] == '\t'): p += 1
                # strip line if it consists of whitespace entirely
                if p >= length - 1: continue
                # peek ahead for correct indent of current line
                next = line[p + 1]
                if line[p] == '<' and next == '/': indent -= 1
                # print indent and the rest of the line
                content.append(' ' * indent)
            content.extend(line[p:])
            # update indent for the next line
            if line[p] == '<' and next != '/' and next != '!':
                indent += 1
                if delimits_preserve_area(line, p+1):
                    do_preserve = True
            elif line[p] == '/' and next == '>': indent -= 1
            while p < length - 2:
                p += 1
                next = line[p + 1]
                if line[p] == '<':
                    if next == '/':
                        if do_preserve and delimits_preserve_area(line, p):
                            do_preserve = False
                        else:
                            indent -= 1
                    elif next == '!': pass
                    else:
                        indent += 1
                        if delimits_preserve_area(line, p+1):
                            do_preserve = True
                elif line[p] == '/' and next == '>': indent -= 1

        # print content
        response.content = (u"".join(content)).encode(settings.DEFAULT_CHARSET)
        return response


thread_locals = threading.local()

def current_user():
    return thread_locals.user

class CurrentUserMiddleware(object):
    """Middleware that gets the user from the request object and saves it in
    thread local storage."""
    def process_request(self, request):
        thread_locals.user = request.user



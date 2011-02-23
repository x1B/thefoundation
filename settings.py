import os
ROOT = os.path.dirname(os.path.abspath(__file__))
path = lambda *parts: os.path.join(ROOT, *parts)

DEBUG = False
DEBUG_JS = False
DEBUG_CSS = False
TEMPLATE_CONTEXT_PROCESSORS = ()
TEMPLATE_DEBUG = False

import logging
LOG_LEVEL = logging.ERROR
LOG_FILE = path("../var/log/thefoundation.log")

ADMINS = () # no e-mail
MANAGERS = ()
SERVER_EMAIL = ""
EMAIL_SUBJECT_PREFIX = ""
SEND_BROKEN_LINK_EMAILS = False

SITE_ID = 1 # for redirects
HOST_NAME = "http://www.thefoundation.de"

TIME_ZONE = "Europe/Berlin"
LANGUAGE_CODE = "en-us"
USE_I18N = False

MEDIA_ROOT = path("media")
MEDIA_URL = "/media/"
ADMIN_MEDIA_PREFIX = "/admin/media/"

DEFAULT_CHARSET = "utf-8"
DEFAULT_CONTENT_TYPE = "text/html"

TEMPLATE_STRING_IF_INVALID = ""
TEMPLATE_LOADERS = (
    "django.template.loaders.filesystem.load_template_source",
    "django.template.loaders.app_directories.load_template_source",
)
TEMPLATE_DIRS = (
    path("%s/templates"),
)
TEMPLATE_CONTEXT_PROCESSORS += (
    "django.core.context_processors.debug",
    "django.core.context_processors.auth",
)

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.admin",
    "django.contrib.humanize",
    "thefoundation.blogging",
    "thefoundation.external.photologue",
)

ROOT_URLCONF = "thefoundation.urls"

MIDDLEWARE_CLASSES = (
    'thefoundation.middleware.exception_handling.LogExceptionsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.cache.CacheMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.common.CommonMiddleware',
    'thefoundation.middleware.CurrentUser',
)

# external/photologue:
PHOTOLOGUE_DIR = "galleries"

# apps/blogging:
FEED_LIMIT = 15 # max entries in atom feed

# Do not edit settings in this file!
# Use a special settings file at startup (such as ...development, ...testing, ...production).

import os
project_root = os.path.abspath( os.path.dirname( __file__ ) )

HOST_NAME = "http://www.thefoundation.de"

DEBUG = False
DEBUG_JS = False
DEBUG_CSS = False
TEMPLATE_CONTEXT_PROCESSORS = ( )
TEMPLATE_DEBUG = False

import logging
LOG_LEVEL = logging.ERROR
LOG_FILE  = "%s/var/log/thefoundation.log" % project_root

## general ##################################################################################################

# no e-mail
ADMINS = ()
MANAGERS = ()
SERVER_EMAIL = ""
EMAIL_SUBJECT_PREFIX = ""
SEND_BROKEN_LINK_EMAILS = False

# for redirects
SITE_ID = 1



## content serving / negotiation ############################################################################

# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = "Europe/Berlin"

# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
LANGUAGE_CODE = "en-us"

USE_I18N = False

MEDIA_ROOT = "%s/media" % project_root

MEDIA_URL = "/media/"

ADMIN_MEDIA_PREFIX = "/admin/media/"

# Make this unique, and don't share it with anybody.
# SECRET_KEY = ...

DEFAULT_CHARSET = "utf-8"

DEFAULT_CONTENT_TYPE = "text/html"



## templates ################################################################################################

TEMPLATE_STRING_IF_INVALID = ""

TEMPLATE_LOADERS = (
    "django.template.loaders.filesystem.load_template_source",
    "django.template.loaders.app_directories.load_template_source",
)

# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
TEMPLATE_DIRS = (
    "%s/templates" % project_root,
)

TEMPLATE_CONTEXT_PROCESSORS += (
    "django.core.context_processors.debug",
    "django.core.context_processors.auth",
)




## applications, urls #######################################################################################

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

# Max. number of entries in Atom feed.
FEED_LIMIT = 15


## application settings #####################################################################################

PHOTOLOGUE_DIR = "galleries"




## middleware ###############################################################################################

# Because django creates multiple instances of our middleware module, we put the threadlocals here.
MIDDLEWARE_CLASSES = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.common.CommonMiddleware",
    "thefoundation.middleware.current_user.ThreadLocals",
)


## database #################################################################################################

# override the necessary paramters depending on your setup
DATABASE_ENGINE = ""
DATABASE_NAME = ""
DATABASE_USER = ""
DATABASE_PASSWORD = ""
DATABASE_HOST = ""
DATABASE_PORT = ""



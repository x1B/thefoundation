import os
ROOT = os.path.dirname(os.path.abspath(__file__))
path = lambda *parts: os.path.join(ROOT, *parts)

DEBUG = False
DEBUG_JS = False
DEBUG_CSS = False
TEMPLATE_CONTEXT_PROCESSORS = ()
TEMPLATE_DEBUG = False

ADMINS = () # no e-mail
MANAGERS = ()
SERVER_EMAIL = ""
EMAIL_SUBJECT_PREFIX = ""
SEND_BROKEN_LINK_EMAILS = False

SITE_ID = 1 # for redirects

TIME_ZONE = "Europe/Berlin"
LANGUAGE_CODE = "en-us"
USE_I18N = False

MEDIA_ROOT = path("media")
MEDIA_URL = "/media/"
ADMIN_MEDIA_PREFIX = "/admin/media/"

DEFAULT_CHARSET = "utf-8"
DEFAULT_CONTENT_TYPE = "text/html"

TEMPLATE_STRING_IF_INVALID = ""
TEMPLATE_DIRS = (
    path('templates'),
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
TEMPLATE_CONTEXT_PROCESSORS += (
    "django.core.context_processors.debug",
    "django.contrib.auth.context_processors.auth",
)

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.admin",
    "django.contrib.humanize",
    "django.contrib.comments",
    "django_nose",
    "blogging",
    "custom_comments",
    "galleries",
    "management",
    "tf",
    "photologue",
)

ROOT_URLCONF = "thefoundation.urls"

MIDDLEWARE_CLASSES = (
    'tf.middleware.LogExceptionsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.cache.CacheMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.common.CommonMiddleware',
    'tf.middleware.CurrentUserMiddleware',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s| %(name)-10s | %(levelname)-5s %(message)s'
        },
    },
    'handlers': {
        'logfile':{
            'level': 'INFO',
            'formatter': 'verbose',
            'class':'logging.FileHandler',
            'filename': path('../log/thefoundation.log'),
        },
    },
    'loggers': {
        '': {
            'handlers': ['logfile'],
            'propagate': True,
            'level':'INFO',
        },
    },
}

# testing
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# external/photologue:
PHOTOLOGUE_DIR = "galleries"

# apps/custom_comments:
COMMENTS_APP = "custom_comments"

# apps/blogging:
FEED_LIMIT = 15

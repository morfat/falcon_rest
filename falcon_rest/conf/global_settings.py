"""
Default  settings. Override these with settings in the module pointed to
by the FALCHEMY_SETTINGS_MODULE environment variable.
"""


DEBUG = False


DB_ENGINE = ''
DATABASE = {}

# List of strings representing installed apps.
INSTALLED_APPS = []


# A secret key for this particular  installation. Used in secret-key
# hashing algorithms. Set this in your settings, or will complain
# loudly.
#jwt
JWT_TOKEN_LIFETIME_WEB=3600 #seconds token is active
JWT_TOKEN_LIFETIME=3600 
JWT_SECRET_KEY = ''


# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

#where url routes are stored
URLS_MODULE = ''


# List of middleware to use. Order is important; in the request phase, these
# middleware will be applied in the order given, and in the response
# phase the middleware will be applied in reverse order.
MIDDLEWARE = []

CURSOR_PAGINATION = {
    'MAX_PAGE_SIZE': 1000,
    'DEFAULT_PAGE_SIZE': 20,
    'PAGE_SIZE_QUERY_PARAM': 'page_size',
    'AFTER_CURSOR_QUERY_PARAM': 'after',
    'BEFORE_CURSOR_QUERY_PARAM': 'before',
    'PAGE_QUERY_PARAM':  'page'
}

SEARCH_QUERY_PARAM_NAME = 'search'

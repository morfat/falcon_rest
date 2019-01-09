"""
Default  settings. Override these with settings in the module pointed to
by the FALCHEMY_SETTINGS_MODULE environment variable.
"""


DEBUG = False


DB_ENGINE = ''
DATABASE = {}

# List of strings representing installed apps.
INSTALLED_APPS = []


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



PAGINATION_PAGE_SIZE = 20

SEARCH_QUERY_PARAM = 'search'
FILTER_QUERY_PARAM = 'filter'
ORDERING_QUERY_PARAM = 'ordering'



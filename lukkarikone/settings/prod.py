"""
PRODUCTION SETTINGS!!
"""

from .common import *

# Common production settings
DEBUG = False

CSRF_COOKIE_SECURE = False          # False to allow logins
SESSION_COOKIE_SECURE = True       
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_SSL_REDIRECT = False         # Needs SSL
CSRF_COOKIE_HTTPONLY = False

# this may need some work
ALLOWED_HOSTS = [".matiasturunen.koding.io", ".herokuapp.com"]

# static files location
STATIC_ROOT = "staticfiles"

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# Production database settings
# 
# production will use postgesql as database
# Parse database configuration from $DATABASE_URL
import dj_database_url

DATABASES['default'] =  dj_database_url.config()

# Enable Persistent Connections
DATABASES['default']['CONN_MAX_AGE'] = 500

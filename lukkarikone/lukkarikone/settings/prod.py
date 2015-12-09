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
ALLOWED_HOSTS = [".matiasturunen.koding.io", ""]

# static files location
STATIC_ROOT = "/home/matiasturunen/Web/lukkarikone-files"
STATIC_URL = 'http://umkk434cba97.matiasturunen.koding.io/lukkarikone-files/'

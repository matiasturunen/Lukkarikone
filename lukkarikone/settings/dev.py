"""
DEV SETTINGS!!
"""

from .common import *

# common dev settings
DEBUG = True

# static files location
STATIC_ROOT = "staticfiles"

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

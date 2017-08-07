#! coding: utf-8
import os
# noinspection PyUnresolvedReferences
from .base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Admin name', 'admin_name@devartis.com'),
)

MANAGERS = ADMINS

# Parse database configuration from $DATABASE_URL
DATABASES = {}
DATABASES['default'] = dj_database_url.config()

#MEDIA_ROOT = env('MEDIA_ROOT')
#STATIC_ROOT = env('STATIC_ROOT')
#SECRET_KEY = env('DJANGO_SECRET_KEY')

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['pompom-prod.herokuapp.com']

RAVEN_CONFIG = {
    'dsn': os.environ['RAVEN_DSN'],
}

INSTALLED_APPS = INSTALLED_APPS + ('raven.contrib.django.raven_compat',)
# static file serving for heroku
MIDDLEWARE += ('whitenoise.middleware.WhiteNoiseMiddleware',)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

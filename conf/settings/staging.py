#! coding: utf-8
import os
import dj_database_url
# noinspection PyUnresolvedReferences
from .base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Fernando Aramendi', 'fernando@devartis.com'),
)

MANAGERS = ADMINS

# Parse database configuration from $DATABASE_URL
DATABASES = {}
DATABASES['default'] = dj_database_url.config()

#MEDIA_ROOT = os.environ['MEDIA_ROOT']
#STATIC_ROOT = os.environ['STATIC_ROOT']

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

RAVEN_CONFIG = {
    'dsn': os.environ['RAVEN_DSN'],
}

INSTALLED_APPS = INSTALLED_APPS + ('raven.contrib.django.raven_compat',)

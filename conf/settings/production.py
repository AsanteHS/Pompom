#! coding: utf-8
import os
import dj_database_url
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

SECRET_KEY = env('DJANGO_SECRET_KEY')
MOBILE_TOKEN_KEY = env('MOBILE_TOKEN_KEY')

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

# Allow all host headers
ALLOWED_HOSTS = ['pompom-prod.herokuapp.com', 'pompomapp.net', 'www.pompomapp.net']

RAVEN_CONFIG = {
    'dsn': os.environ['RAVEN_DSN'],
}

INSTALLED_APPS = INSTALLED_APPS + \
                 ('raven.contrib.django.raven_compat',
                  'storages',)
MIDDLEWARE = MIDDLEWARE + \
    ('django.middleware.security.SecurityMiddleware',)


AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'pompom.libs.custom_storages.StaticStorage'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)

MEDIAFILES_LOCATION = 'media'
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'pompom.libs.custom_storages.MediaStorage'
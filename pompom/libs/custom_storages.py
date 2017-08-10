from django.conf import settings
from storages.backends.s3boto import S3BotoStorage


class StaticStorage(S3BotoStorage):
    def path(self, name):
        pass

    location = settings.STATICFILES_LOCATION


class MediaStorage(S3BotoStorage):
    def path(self, name):
        pass

    location = settings.MEDIAFILES_LOCATION

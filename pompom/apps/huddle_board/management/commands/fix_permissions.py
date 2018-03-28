from __future__ import unicode_literals, absolute_import, division

import sys

from django.contrib.auth.management import _get_all_permissions
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.apps import apps
from django.utils.encoding import smart_text


def fix(self, *args, **options):
    for model in apps.get_models():
        opts = model._meta
        ctype, created = ContentType.objects.get_or_create(
            app_label=opts.app_label,
            model=opts.object_name.lower())
        for codename, name in _get_all_permissions(opts):
            perm, created = Permission.objects.get_or_create(
                codename=codename,
                content_type=ctype,
                defaults={'name': name})
            if created:
                sys.stdout.write('Adding permission {}\n'.format(p))

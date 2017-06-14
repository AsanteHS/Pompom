#! coding: utf-8
# pylint:disable=W0613
from django.db.models import Field
from django.utils.translation import ugettext as _


class EmbeddedMultiCharField(Field):
    """
    This is an example of the kind of classes that can be sent to the lib directory.
    """
    description = _("EmbeddedMultiChar")

    def get_internal_type(self):
        return "TextField"

    def from_db_value(self, value, expression, connection, context):
        if not value:
            return None

        return value.split("|")

    def get_prep_value(self, value):
        if not value or value == "":
            return None

        return '|'.join([a_value.strip() for a_value in value])

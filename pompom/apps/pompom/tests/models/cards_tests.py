import pytest
from django.test import TestCase

from pompom.apps.pompom.models import Card


@pytest.mark.django_db
class TestDocument:

    @pytest.fixture
    def a_card(self):
        title = "card title"
        return Card.objects.create(title=title)

    def test_card_as_string(self, a_card):
        assert str(a_card) == "card title"

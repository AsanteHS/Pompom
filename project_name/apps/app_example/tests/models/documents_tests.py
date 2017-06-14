# coding=utf-8
import pytest
from project_name.apps.app_example.models import Document


@pytest.mark.django_db
class TestDocument:

    @pytest.fixture
    def a_document(self):
        title = "long document title"
        return Document.objects.create(title=title)

    def test_document_short_title(self, a_document):
        assert a_document.short_title() == "long"

# coding=utf-8
import pytest
from project_name.apps.app_example.models import Document

@pytest.fixture
def a_document():
    title = "long document title"
    return Document.objects.create(title=title)

@pytest.mark.django_db
class TestDocument:

    def test_document_short_title(self, a_document):
        assert "long" == a_document.short_title()

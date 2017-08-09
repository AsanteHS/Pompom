import pytest

from pompom.apps.huddle_board.models import Card, CardSection


@pytest.mark.django_db
class TestCard:

    @pytest.fixture
    def a_card(self):
        title = "card title"
        return Card.objects.create(title=title)

    @pytest.fixture
    def some_card_sections(self, a_card):
        return [CardSection.objects.create(
            title="Section {}".format(number),
            contents="Some text",
            card=a_card,
            is_gradable=True,
        ) for number in ['one', 'two', 'three']]

    def test_card_as_string(self, a_card):
        assert str(a_card) == "card title"

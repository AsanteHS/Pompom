import pytest

from pompom.apps.huddle_board.models import Card, Board, Deck


@pytest.mark.django_db
class TestBoard:

    @pytest.fixture
    def three_cards(self):
        return [Card.objects.create(title="card {}".format(number)) for number in ['one', 'two', 'three']]

    @pytest.fixture
    def a_deck(self, three_cards):
        deck = Deck.objects.create(title="a deck")
        deck.cards.set(three_cards)
        return deck

    @pytest.fixture
    def a_board(self, a_deck):
        return Board.objects.create(title='a board', deck=a_deck)

    @pytest.fixture
    def a_different_board(self, a_deck):
        return Board.objects.create(title='a different board', deck=a_deck)

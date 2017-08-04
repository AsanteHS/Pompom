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

    def test_draw_card_returns_each_card_from_deck(self, a_board, three_cards):
        three_drawn_cards = {a_board.draw_card() for _ in range(3)}
        assert three_drawn_cards == set(three_cards)

    def test_fourth_drawn_card_causes_reshuffle(self, a_board, three_cards):
        for _ in range(3):
            a_board.draw_card()
        fourth_drawn_card = a_board.draw_card()
        assert fourth_drawn_card in three_cards

    def test_shuffle_board(self, a_board):
        a_board.reshuffle()
        assert a_board.draw_pile.count() == 3

import pytest

from pompom.apps.huddle_board.models import Card, Board, Deck, Observation, CardSection, Answer


@pytest.mark.django_db
class TestBoard:

    @pytest.fixture
    def a_card(self):
        return Card.objects.create(title="card zero")

    @pytest.fixture
    def three_cards(self):
        return [Card.objects.create(title="card {}".format(number)) for number in ['one', 'two', 'three']]

    @pytest.fixture
    def an_empty_deck(self):
        return Deck.objects.create(title="an empty deck")

    @pytest.fixture
    def a_deck(self, a_card, three_cards):
        deck = Deck.objects.create(title="a deck")
        deck.cards.set(three_cards + [a_card])
        return deck

    @pytest.fixture
    def a_board_with_empty_deck(self, an_empty_deck):
        return Board.objects.create(title='a board with empty deck', deck=an_empty_deck)

    @pytest.fixture
    def a_board(self, a_deck):
        return Board.objects.create(title='a board', deck=a_deck)

    @pytest.fixture
    def a_board_with_no_deck(self):
        return Board.objects.create(title='a board with no deck')

    @pytest.fixture
    def a_different_board(self, a_deck):
        return Board.objects.create(title='a different board', deck=a_deck)

    @pytest.fixture
    def some_observations(self, a_board, a_card):
        section = CardSection.objects.create(card=a_card, is_gradable=True)
        observations = []
        for grade in [True, False, None]:
            observation = Observation.objects.create(board=a_board, card=a_card)
            observations.append(observation)
            Answer.objects.create(observation=observation, card_section=section, grade=grade)
        return observations

    def test_result_history_with_no_deck_returns_empty_list(self, a_board_with_no_deck):
        assert [] == a_board_with_no_deck.result_history()

    def test_result_history_with_empty_deck_returns_empty_list(self, a_board_with_empty_deck):
        assert [] == a_board_with_empty_deck.result_history()

    def test_result_history_with_cards_returns_tuple_for_each_card(self, a_board):
        results = a_board.result_history()
        result_cards = set([card for card, _ in results])
        cards_in_deck = set(a_board.deck.cards.all())
        assert cards_in_deck == result_cards

    def test_result_history_shows_graded_observations_for_a_card(self, a_board, a_card, some_observations):
        results = a_board.result_history()
        card_zero, card_zero_results = results[0]
        some_observations.reverse()  # sorting observations by descending datetime
        observation_grades = [observation.grade() for observation in some_observations]

        assert a_card == card_zero
        assert observation_grades == card_zero_results

    def test_history_ignores_observations_from_different_boards(self, a_different_board, a_card, some_observations):
        results = a_different_board.result_history()
        card_zero, card_zero_results = results[0]

        for observation in some_observations:
            assert a_different_board != observation.board
        assert a_card == card_zero
        assert [] == card_zero_results

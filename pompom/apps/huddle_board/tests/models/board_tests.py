from datetime import timedelta
from unittest import mock

import pytest
from django.utils import timezone

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

    @pytest.fixture
    def an_old_observation(self, a_board, a_card):
        forty_days_ago = timezone.now() - timedelta(days=40)
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = forty_days_ago
            observation = Observation.objects.create(board=a_board, card=a_card)
        return observation

    def test_result_history_with_no_deck_returns_empty_list(self, a_board_with_no_deck):
        assert [] == a_board_with_no_deck.result_history()

    def test_result_history_with_empty_deck_returns_empty_list(self, a_board_with_empty_deck):
        assert [] == a_board_with_empty_deck.result_history()

    def test_result_history_with_cards_returns_tuple_for_new_cards(self, a_board, some_observations):
        results = a_board.result_history()
        result_cards = set([card for card, _, _ in results])
        observation_cards = set([observation.card for observation in some_observations])

        assert observation_cards == result_cards

    def test_result_history_shows_graded_observations_for_a_card(self, a_board, a_card, some_observations):
        results = a_board.result_history()
        card_zero, card_zero_results, _ = results[0]
        observation_grades = [observation.grade() for observation in some_observations]

        assert a_card == card_zero
        assert observation_grades == card_zero_results

    def test_history_ignores_observations_from_different_boards(self, a_board, a_different_board, some_observations):
        results_a_different_board = a_different_board.result_history()
        results_a_board = a_board.result_history()
        results_a_board_cards = set([card for card, _, _ in results_a_board])

        for observation in some_observations:
            assert a_different_board != observation.board
            assert observation.card in results_a_board_cards
        assert results_a_different_board == []

    @pytest.mark.usefixtures("an_old_observation")
    def test_history_ignores_observations_older_than_thirty_days(self, a_board):
        results = a_board.result_history()

        assert a_board.observations != []
        assert [] == results

    def test_result_history_shows_success_ratio_for_a_card(self, a_board, a_card, some_observations):
        results = a_board.result_history()
        card_zero, _, success_rate = results[0]
        grades = [observation.grade() for observation in some_observations]
        passing = grades.count(True)

        assert a_card == card_zero
        assert passing / float(len(grades)) == success_rate

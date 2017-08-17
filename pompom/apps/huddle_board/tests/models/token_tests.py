from datetime import timedelta
from unittest import mock

import pytest
from django.utils import timezone

from pompom.libs.tokens import MobileToken


class TestTokens:

    @pytest.fixture
    def a_token(self):
        return MobileToken()

    @pytest.fixture
    def a_token_after_almost_twelve_hours(self):
        almost_twelve_hours_ago = timezone.now() - timedelta(hours=11, minutes=50)
        return self.generate_token_from_datetime(almost_twelve_hours_ago)

    @pytest.fixture
    def a_token_after_more_than_twelve_hours(self):
        more_than_twelve_hours_ago = timezone.now() - timedelta(hours=12, minutes=10)
        return self.generate_token_from_datetime(more_than_twelve_hours_ago)

    @pytest.fixture
    def a_token_string(self):
        token = MobileToken()
        return token.ciphertext

    def generate_token_from_datetime(self, datetime):
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = datetime
            token = MobileToken()
        return token

    def test_token_is_valid_after_generation(self, a_token):
        assert not a_token.expired()

    def test_token_is_valid_for_twelve_hours(self, a_token_after_almost_twelve_hours):
        assert not a_token_after_almost_twelve_hours.expired()

    def test_token_is_invalid_after_twelve_hours(self, a_token_after_more_than_twelve_hours):
        assert a_token_after_more_than_twelve_hours.expired()

    def test_token_from_received_string_is_valid(self, a_token_string):
        token = MobileToken(a_token_string)
        assert not token.expired()

    def test_token_from_random_string_is_invalid(self):
        some_arbitrary_string = b'34563857683945836453453453'
        token = MobileToken(some_arbitrary_string)
        assert token.expired()

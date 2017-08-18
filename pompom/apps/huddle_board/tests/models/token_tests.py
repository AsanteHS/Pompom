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
    def a_token_created_today_at_five_a_m(self):
        return self.generate_token_today_at_hour(5)

    @pytest.fixture
    def a_token_created_today_at_nine_a_m(self):
        return self.generate_token_today_at_hour(9)

    @pytest.fixture
    def a_token_created_today_at_ten_p_m(self):
        return self.generate_token_today_at_hour(22)

    def generate_token_today_at_hour(self, hour):
        toady_at_hour = timezone.now().replace(hour=hour, minute=0, second=0, microsecond=0)
        return self.generate_token_from_datetime(toady_at_hour)

    def generate_token_from_datetime(self, datetime):
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = datetime
            token = MobileToken()
        return token

    @pytest.fixture
    def a_token_string(self):
        token = MobileToken()
        return token.ciphertext

    def test_token_generated_at_five_will_expire_at_seven(self, a_token_created_today_at_five_a_m):
        seven_a_m = timezone.now().replace(hour=7, minute=0, second=0, microsecond=0)
        assert seven_a_m == a_token_created_today_at_five_a_m.expiration

    def test_token_generated_at_nine_will_expire_at_seven_p_m(self, a_token_created_today_at_nine_a_m):
        seven_p_m = timezone.now().replace(hour=19, minute=0, second=0, microsecond=0)
        assert seven_p_m == a_token_created_today_at_nine_a_m.expiration

    def test_token_generated_at_night_will_expire_early_tomorrow(self, a_token_created_today_at_ten_p_m):
        seven_a_m_tomorrow = timezone.now().replace(hour=7, minute=0, second=0, microsecond=0) + timedelta(days=1)
        assert seven_a_m_tomorrow == a_token_created_today_at_ten_p_m.expiration

    def test_token_is_valid_after_generation(self, a_token):
        assert not a_token.expired()

    def test_token_is_valid_before_expiration(self, a_token_created_today_at_five_a_m):
        today_at_six = timezone.now().replace(hour=6, minute=0, second=0, microsecond=0)
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = today_at_six
            assert not a_token_created_today_at_five_a_m.expired()

    def test_token_is_invalid_after_expiration(self, a_token_created_today_at_five_a_m):
        today_at_eight = timezone.now().replace(hour=8, minute=0, second=0, microsecond=0)
        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = today_at_eight
            assert a_token_created_today_at_five_a_m.expired()

    def test_token_built_from_received_string_is_valid(self, a_token_string):
        token = MobileToken(a_token_string)
        assert not token.expired()

    def test_token_built_from_random_string_is_invalid(self):
        some_arbitrary_string = 'AAADDwUCwQcNAA=='
        token = MobileToken(some_arbitrary_string)
        assert token.expired()

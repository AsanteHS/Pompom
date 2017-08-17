import base64
from datetime import timedelta, datetime

import binascii
from Crypto.Cipher import XOR
from django.conf import settings
from django.utils import timezone, dateformat

HOURS_UNTIL_TOKEN_EXPIRY = 12


class MobileToken:

    def __init__(self, ciphertext=None):
        if ciphertext is None:
            self.datetime = timezone.now() + timedelta(hours=HOURS_UNTIL_TOKEN_EXPIRY)
            self.ciphertext = self.datetime_to_ciphertext()
        else:
            self.ciphertext = ciphertext
            self.datetime = self.ciphertext_to_datetime()

    def datetime_to_ciphertext(self):
        expiry_timestamp = dateformat.format(self.datetime, 'U')
        byte_array = encrypt(settings.MOBILE_TOKEN_KEY, expiry_timestamp)
        return byte_array.decode("utf-8")

    def ciphertext_to_datetime(self):
        byte_array = self.ciphertext.encode("utf-8")
        try:
            token_timestamp = int(decrypt(settings.MOBILE_TOKEN_KEY, byte_array))
        except (binascii.Error, ValueError):
            min_datetime = timezone.make_aware(datetime.min + timedelta(days=1), timezone.get_current_timezone())
            return min_datetime
        return datetime.fromtimestamp(token_timestamp, tz=timezone.get_current_timezone())

    def expired(self):
        return self.datetime < timezone.now()


def encrypt(key, plaintext):
    cipher = XOR.new(key)
    return base64.urlsafe_b64encode(cipher.encrypt(plaintext))


def decrypt(key, ciphertext):
    cipher = XOR.new(key)
    return cipher.decrypt(base64.urlsafe_b64decode(ciphertext))

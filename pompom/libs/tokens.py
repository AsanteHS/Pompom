import base64
from datetime import timedelta, datetime

from Crypto.Cipher import XOR
from django.utils import timezone, dateformat

HOURS_UNTIL_TOKEN_EXPIRY = 12
QR_TOKEN_KEY = '12345'


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
        return encrypt(QR_TOKEN_KEY, expiry_timestamp)

    def ciphertext_to_datetime(self):
        token_timestamp = int(decrypt(QR_TOKEN_KEY, self.ciphertext))
        return datetime.fromtimestamp(token_timestamp, tz=timezone.get_current_timezone())

    def expired(self):
        return self.datetime < timezone.now()


def encrypt(key, plaintext):
    cipher = XOR.new(key)
    return base64.b64encode(cipher.encrypt(plaintext))


def decrypt(key, ciphertext):
    cipher = XOR.new(key)
    return cipher.decrypt(base64.b64decode(ciphertext))

#handles TOTP (Time-based One-Time Password) code calculation for Discord. Discord's totp refreshes every 30 seconds.
#implementation is the same as https://github.com/pyauth/pyotp/ (most of the functions are just copy-pasted)

import time, datetime
import hmac
import base64
import hashlib

class TOTP:
    def __init__(self, secret):
        self.secret = secret

    def byte_secret(self):
        missing_padding = len(self.secret) % 8
        if missing_padding != 0:
            self.secret += '=' * (8 - missing_padding)
        return base64.b32decode(self.secret, casefold=True)

    @staticmethod
    def int_to_bytestring(i, padding=8):
        """
        Turns an integer to the OATH specified
        bytestring, which is fed to the HMAC
        along with the secret
        """
        result = bytearray()
        while i != 0:
            result.append(i & 0xFF)
            i >>= 8
        return bytes(bytearray(reversed(result)).rjust(padding, b'\0'))

    def generateTOTP(self):
        timecode = int(time.mktime(datetime.datetime.now().timetuple())/30)
        hasher = hmac.new(self.byte_secret(), self.int_to_bytestring(timecode), hashlib.sha1)
        hmac_hash = bytearray(hasher.digest())
        offset = hmac_hash[-1] & 0xf
        code = ((hmac_hash[offset] & 0x7f) << 24 |
                (hmac_hash[offset + 1] & 0xff) << 16 |
                (hmac_hash[offset + 2] & 0xff) << 8 |
                (hmac_hash[offset + 3] & 0xff))
        codelength = 6
        str_code = str(code % 10 ** codelength)
        while len(str_code) < codelength:
            str_code = '0' + str_code
        return str_code
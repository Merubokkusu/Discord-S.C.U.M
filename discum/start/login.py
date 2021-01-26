from ..RESTapiwrap import *
from .totp import TOTP
import requests
import time

class Login:
    '''
    Manages HTTP authentication
    '''
    def __init__(self, s, discordurl, log):
        self.s = s
        self.discord = discordurl
        self.log = log
        if 'Authorization' in s.headers or 'X-Fingerprint' in s.headers:
            self.editedS = requests.Session()
            self.editedS.headers.update(s.headers)
            if 'Authorization' in self.editedS.headers:
                del self.editedS.headers['Authorization']
            if 'X-Fingerprint' in self.editedS.headers:
                del self.editedS.headers['X-Fingerprint']
            self.editedS.proxies.update(s.proxies)
        else:
            self.editedS = s

    def GetXFingerprint(self):
        url = self.discord + "experiments"
        reqxfinger = Wrapper.sendRequest(self.editedS, 'get', url, log=self.log)
        xfingerprint = json.loads(reqxfinger.content).get('fingerprint')
        if self.log:
            if xfingerprint == None:
                print('xfingerprint could not be fetched.')
        return xfingerprint

    def GetToken(self, email, password, undelete=False, captcha=None, source=None, gift_code_sku_id=None, secret="", code=""):
        url = self.discord + "auth/login"
        self.xfingerprint = self.GetXFingerprint()
        self.s.headers.update({"X-Fingerprint": self.xfingerprint})
        self.editedS.headers.update({"X-Fingerprint": self.xfingerprint})
        body = {
            "email": email,
            "password": password,
            "undelete": undelete,
            "captcha_key": captcha,
            "login_source": source,
            "gift_code_sku_id": gift_code_sku_id
        }
        response = Wrapper.sendRequest(self.editedS, 'post', url, body, log=self.log)
        result = json.loads(response.content)
        if 'mfa' in result and 'sms' in result: #sms login not implemented yet
            if result['mfa'] == True and result['sms'] == False:
                time.sleep(2) #2 seconds is minimal, don't want to look too automated
                ticket = result['ticket']
                if secret != "":
                    code = TOTP(secret).generateTOTP()
                code = str(code) #just in case an int is inputted
                totpUrl = self.discord+"auth/mfa/totp"
                totpBody = {
                    "code": code,
                    "ticket": ticket,
                    "login_source": source,
                    "gift_code_sku_id": gift_code_sku_id
                }
                totpResponse = Wrapper.sendRequest(self.editedS, 'post', totpUrl, totpBody, log=self.log)
                result = json.loads(totpResponse.content)
        self.__token = result['token']
        return self.__token, self.xfingerprint

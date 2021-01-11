from ..RESTapiwrap import *

class Login:
    '''
    Manages HTTP authentication
    '''
    def __init__(self, s, discordurl, log):
        self.s = s
        self.discord = discordurl
        self.log = log

    def GetXFingerprint(self):
        url = self.discord + "experiments"
        reqxfinger = Wrapper.sendRequest(self.s, 'get', url, log=self.log)
        xfingerprint = json.loads(reqxfinger.content)['fingerprint']
        return xfingerprint

    def GetToken(self, email, password, undelete=False, captcha=None, source=None, gift_code_sku_id=None):
        url = self.discord + "auth/login"
        self.xfingerprint = self.GetXFingerprint()
        self.s.headers.update({"X-Fingerprint": self.xfingerprint})
        body = {
            "email": email,
            "password": password,
            "undelete": undelete,
            "captcha_key": captcha,
            "login_source": source,
            "gift_code_sku_id": gift_code_sku_id,
        }
        response = Wrapper.sendRequest(self.s, 'post', url, body, log=self.log)
        self.__token = json.loads(response.content)['token']
        return self.__token, self.xfingerprint

from ..RESTapiwrap import *
import requests

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

    def GetToken(self, email, password, undelete=False, captcha=None, source=None, gift_code_sku_id=None):
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
            "gift_code_sku_id": gift_code_sku_id,
        }
        response = Wrapper.sendRequest(self.editedS, 'post', url, body, log=self.log)
        self.__token = json.loads(response.content)['token']
        return self.__token, self.xfingerprint

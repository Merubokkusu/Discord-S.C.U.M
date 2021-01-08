from ..RESTapiwrap import *

class Login:
    '''
    Manages HTTP authentication
    '''
    def __init__(self, s, discordurl, user_email, user_password, log):
        self.s = s
        self.discord = discordurl
        self.__user_email = user_email
        self.__user_password = user_password
        self.log = log
        self.__token = None

    def GetXFingerprint(self):
        url = self.discord + "experiments"
        reqxfinger = Wrapper.sendRequest(self.s, 'get', url, log=self.log)
        xfingerprint = json.loads(reqxfinger.content)['fingerprint']
        return xfingerprint

    def Connect(self):
        url = self.discord + "auth/login"
        self.xfingerprint = self.GetXFingerprint()
        self.s.headers.update({"X-Fingerprint": self.xfingerprint})
        body = {"email": self.__user_email, "password": self.__user_password, "undelete": False, "captcha_key": None, "login_source": None, "gift_code_sku_id": None}
        response = Wrapper.sendRequest(self.s, 'post', url, body, log=self.log)
        self.__token = json.loads(response.content)['token']

    def GetToken(self):
        if self.__token is None:
            self.Connect()
        return self.__token, self.xfingerprint

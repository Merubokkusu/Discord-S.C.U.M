from ..Logger import *
import requests
#import requests[socks] #youll need to pip install requests[socks] (this is only if youre using socks)
import json

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
        if self.log: Logger.LogMessage('Get -> {}'.format(url))
        reqxfinger = self.s.get(url)
        if self.log: Logger.LogMessage('Response <- {}'.format(reqxfinger.text), log_level=LogLevel.OK)
        xfingerprint = json.loads(reqxfinger.content)['fingerprint']
        return xfingerprint

    def Connect(self):
        url = self.discord + "auth/login"
        self.xfingerprint = self.GetXFingerprint()
        self.s.headers.update({"X-Fingerprint": self.xfingerprint})
        http_auth_data = '{{"email": "{}", "password": "{}", "undelete": false, "captcha_key": null, "login_source": null, "gift_code_sku_id": null}}'.format(self.__user_email, self.__user_password)
        if self.log: Logger.LogMessage('Post -> {}'.format(url))
        if self.log: Logger.LogMessage('{}'.format(http_auth_data))
        response = self.s.post(url, data=http_auth_data)
        if self.log: Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
        self.__token = json.loads(response.content)['token']

    def GetToken(self):
        if self.__token is None:
            self.Connect()
        return self.__token, self.xfingerprint

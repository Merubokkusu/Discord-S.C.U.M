from .Logger import *
import requests
#import requests[socks] #youll need to pip install requests[socks] (this is only if youre using socks)
import json

class Login:
    '''
    Manages HTTP authentication
    '''
    URL = "https://discordapp.com/api/v8/auth/login" #self.URL

    def __init__(self, user_email, user_password,proxy_host,proxy_port):
        self.__user_email = user_email
        self.__user_password = user_password
        self.__proxy_host = proxy_host
        self.__proxy_port = proxy_port
        self.__token = None

    def Connect(self):
        session = requests.Session()
        if self.__proxy_host != False and self.__proxy_port != False:
            proxies = {
            'http': self.__proxy_host+':'+self.__proxy_port,
            'https': self.__proxy_host+':'+self.__proxy_port
            }
            session.proxies.update(proxies)
        session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.305 Chrome/69.0.3497.128 Electron/4.0.8 Safari/537.36"})
        session.headers.update({'X-Super-Properties': ''})
        session.headers.update({"Content-Type": "application/json"})
        http_auth_data = '{{"email": "{}", "password": "{}", "undelete": false, "captcha_key": null, "login_source": null, "gift_code_sku_id": null}}'.format(self.__user_email, self.__user_password)
        Logger.LogMessage('Post -> {}'.format(self.URL))
        Logger.LogMessage('{}'.format(http_auth_data))
        response = session.post(self.URL, data=http_auth_data)
        Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
        self.__token = json.loads(response.content)['token']

    def GetToken(self):
        if self.__token is None:
            self.Connect()
        return self.__token

from ..Logger import *
import requests
#import requests[socks] #youll need to pip install requests[socks] (this is only if youre using socks)
import json

class Login:
    '''
    Manages HTTP authentication
    '''
    def __init__(self, discordurlstart, user_email, user_password,user_agent,proxy_host,proxy_port,log):
        self.log = log
        self.URL = discordurlstart + "auth/login"
        self.__user_email = user_email
        self.__user_password = user_password
        self.__user_agent = user_agent
        self.__proxy_host = proxy_host
        self.__proxy_port = proxy_port
        self.__token = None

    def Connect(self):
        session = requests.Session()
        if self.__proxy_host not in (None,False):
            proxies = {
            'http': self.__proxy_host+':'+self.__proxy_port,
            'https': self.__proxy_host+':'+self.__proxy_port
            }
            session.proxies.update(proxies)
        session.headers.update({"User-Agent": self.__user_agent})
        session.headers.update({'X-Super-Properties': ''})
        session.headers.update({"Content-Type": "application/json"})
        http_auth_data = '{{"email": "{}", "password": "{}", "undelete": false, "captcha_key": null, "login_source": null, "gift_code_sku_id": null}}'.format(self.__user_email, self.__user_password)
        if self.log: Logger.LogMessage('Post -> {}'.format(self.URL))
        if self.log: Logger.LogMessage('{}'.format(http_auth_data))
        response = session.post(self.URL, data=http_auth_data)
        if self.log: Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
        self.__token = json.loads(response.content)['token']

    def GetToken(self):
        if self.__token is None:
            self.Connect()
        return self.__token

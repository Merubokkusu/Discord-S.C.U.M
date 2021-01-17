from ..RESTapiwrap import *

#This file includes apis that run when your client starts but idk where to organize them
#Maybe they'll get organized eventually, idk
class Other:
    def __init__(self, s, discordurl, log):
        self.s = s
        self.discord = discordurl
        self.log = log

    def getGatewayUrl(self):
        url = self.discord + "gateway"
        return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

    def getDiscordStatus(self):
        url = "https://status.discord.com/api/v2/scheduled-maintenances/upcoming.json"
        return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

    def getDetectables(self):
        url = self.discord + "applications/detectable"
        return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

    def getOauth2Tokens(self):
        url = self.discord + "oauth2/tokens"
        return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

    def getVersionStableHash(self, underscore=None):
        if isinstance(underscore, int):
            underscore = str(underscore)
        url = "https://discord.com/assets/version.stable.json"
        if isinstance(underscore, str):
            url += "?_="+underscore
        return Wrapper.sendRequest(self.s, 'get', url, log=self.log)
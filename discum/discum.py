from .guild.guild import Guild
from .messages.messages import Messages
from .messages.embed import Embedder
from .user.user import User

from .login.Login import *
from .gateway.gateway import *

import time
import random
import re
import user_agents

class SessionSettingsError(Exception):
    pass

class Client:
    def __init__(self, email="none", password="none", token="none", proxy_host=None, proxy_port=None, user_agent="random", log=True): #not using None on email, pass, and token since that could get flagged by discord...
        self.log = log
        self.__user_token = token
        self.__user_email = email
        self.__user_password = password
        self.__proxy_host = None if proxy_host in (None,False) else proxy_host
        self.__proxy_port = None if proxy_host in (None,False) else proxy_host
        self.session_settings = [] #consists of 2 parts, READY and READY_SUPPLEMENTAL
        self.discord = 'https://discord.com/api/v8/'
        self.websocketurl = 'wss://gateway.discord.gg/?encoding=json&v=8'
        if user_agent != "random":
            self.__user_agent = user_agent
        else:
            from random_user_agent.user_agent import UserAgent #only really want to import this if needed...which is why it's down here
            self.__user_agent = UserAgent(limit=100).get_random_user_agent()
            if self.log: print('Randomly generated user agent: '+self.__user_agent)
        parseduseragent = user_agents.parse(self.__user_agent)
        self.ua_data = {'os':parseduseragent.os.family,'browser':parseduseragent.browser.family,'device':parseduseragent.device.family if parseduseragent.is_mobile else '','browser_user_agent':self.__user_agent,'browser_version':parseduseragent.browser.version_string,'os_version':parseduseragent.os.version_string}
        if self.__user_token in ("none",None,False): #assuming email and pass are given...
            self.__login = Login(self.discord,self.__user_email,self.__user_password,self.__user_agent,self.__proxy_host,self.__proxy_port,self.log)
            self.__user_token = self.__login.GetToken() #update token from "none" to true string value
            time.sleep(1)
        self.headers = {
        "Host": "discord.com",
        "User-Agent": self.__user_agent,
        "Accept": "*/*",
        "Accept-Language": "en-US",
        "Authorization": self.__user_token,
        "Connection": "keep-alive",
        "keep-alive" : "timeout=10, max=1000",
        "TE": "Trailers",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Referer": "https://discord.com/channels/@me",
        "Content-Type": "application/json"
        }
        self.s = requests.Session()
        self.s.headers.update(self.headers)
        if self.__proxy_host != None: #self.s.proxies defaults to {}
            self.proxies = {
            'http': self.__proxy_host+':'+self.__proxy_port,
            'https': self.__proxy_host+':'+self.__proxy_port
            }
            self.s.proxies.update(proxies)
        if self.log: print("Retrieving Discord's build number...")
        discord_login_page_exploration = self.s.get('https://discord.com/login').text
        time.sleep(1)
        try: #getting the build num is kinda experimental since who knows if discord will change where the build number is located...
            file_with_build_num = 'https://discord.com/assets/'+re.compile(r'assets/+([a-z0-9]+)\.js').findall(discord_login_page_exploration)[-2]+'.js' #fastest solution I could find since the last js file is huge in comparison to 2nd from last
            req_file_build = self.s.get(file_with_build_num).text
            index_of_build_num = req_file_build.find('buildNumber')+14
            self.discord_build_num = int(req_file_build[index_of_build_num:index_of_build_num+5])
            self.ua_data['build_num'] = self.discord_build_num #putting this onto ua_data since getting the build num won't necessarily work
            if self.log: print('Discord is currently on build number '+str(self.discord_build_num))
        except:
            if self.log: print('Could not retrieve discord build number.')
        self.gateway = GatewayServer(self.websocketurl, self.__user_token, self.ua_data, self.__proxy_host, self.__proxy_port, self.log)

    '''
    test connection (this function was originally in discum and was created by Merubokkusu)
    '''
    def connectionTest(self): #,proxy):
        url=self.discord+'users/@me/affinities/users'
        connection = self.s.get(url)
        if(connection.status_code == 200):
            if self.log: print("Connected")
        else:
            if self.log: print("Incorrect Token")
        return connection

    '''
    discord snowflake to unix timestamp and back
    '''
    def snowflake_to_unixts(self,snowflake):
        return int((snowflake/4194304+1420070400000)/1000)

    def unixts_to_snowflake(self,unixts):
        return int((unixts*1000-1420070400000)*4194304)

    '''
    Messages
    '''
    #create DM
    def createDM(self,recipients):
        return Messages(self.discord,self.s,self.log).createDM(recipients)

    #get recent messages
    def getMessages(self,channelID,num=1,beforeDate=None,aroundMessage=None): # num <= 100, beforeDate is a snowflake
        return Messages(self.discord,self.s,self.log).getMessages(channelID,num,beforeDate,aroundMessage)

    #send text or embed messages
    def sendMessage(self,channelID,message,embed="",tts=False):
        return Messages(self.discord,self.s,self.log).sendMessage(channelID,message,embed,tts)

    #send files (local or link)
    def sendFile(self,channelID,filelocation,isurl=False,message=""):
        return Messages(self.discord,self.s,self.log).sendFile(channelID,filelocation,isurl,message)

    #search messages
    def searchMessages(self,guildID,channelID=None,userID=None,mentionsUserID=None,has=None,beforeDate=None,afterDate=None,textSearch=None,afterNumResults=None):
        return Messages(self.discord,self.s,self.log).searchMessages(guildID,channelID,userID,mentionsUserID,has,beforeDate,afterDate,textSearch,afterNumResults)

    #filter searchMessages, takes in the output of searchMessages (a requests response object) and outputs a list of target messages
    def filterSearchResults(self,searchResponse):
        return Messages(self.discord,self.s,self.log).filterSearchResults(searchResponse)

    #sends the typing action for 10 seconds (or technically until you change the page)
    def typingAction(self,channelID):
        return Messages(self.discord,self.s,self.log).typingAction(channelID)

    #delete message
    def deleteMessage(self,channelID,messageID):
        return Messages(self.discord,self.s,self.log).deleteMessage(channelID,messageID)

    #edit message
    def editMessage(self,channelID,messageID,newMessage):
        return Messages(self.discord,self.s,self.log).editMessage(channelID, messageID, newMessage)

    #pin message
    def pinMessage(self,channelID,messageID):
        return Messages(self.discord,self.s,self.log).pinMessage(channelID,messageID)

    #un-pin message
    def unPinMessage(self,channelID,messageID):
        return Messages(self.discord,self.s,self.log).unPinMessage(channelID,messageID)

    #get pinned messages
    def getPins(self,channelID):
        return Messages(self.discord,self.s,self.log).getPins(channelID)

    #add reaction
    def addReaction(self,channelID,messageID,emoji):
        return Messages(self.discord,self.s,self.log).addReaction(channelID,messageID,emoji)

    #remove reaction
    def removeReaction(self,channelID,messageID,emoji):
        return Messages(self.discord,self.s,self.log).removeReaction(channelID,messageID,emoji)

    #acknowledge message (mark message read)
    def ackMessage(self,channelID,messageID,ackToken=None):
        return Messages(self.discord,self.s,self.log).ackMessage(channelID,messageID,ackToken)

    #unacknowledge message (mark message unread)
    def unAckMessage(self,channelID,messageID,numMentions=0):
        return Messages(self.discord,self.s,self.log).unAckMessage(channelID,messageID,numMentions)

    '''
    User relationships
    '''
    #create outgoing friend request
    def requestFriend(self,user): #you can input a userID(snowflake) or a user discriminator
        return User(self.discord,self.s,self.log).requestFriend(user)

    #accept incoming friend request
    def acceptFriend(self,userID):
        return User(self.discord,self.s,self.log).acceptFriend(userID)

    #remove friend OR unblock user
    def removeRelationship(self,userID):
        return User(self.discord,self.s,self.log).removeRelationship(userID)

    #block user
    def blockUser(self,userID):
        return User(self.discord,self.s,self.log).blockUser(userID)

    '''
    Profile edits
    '''
    # change name
    def changeName(self,name):
        return User(self.discord,self.s,self.log).changeName(self.email,self.password,name)
    # set status
    def setStatus(self,status):
        return User(self.discord,self.s,self.log).setStatus(status)
    # set avatar
    def setAvatar(self,imagePath):
        return User(self.discord,self.s,self.log).setAvatar(self.email,self.password,imagePath)

    '''
    Guild/Server stuff
    '''
    #get guild info from invite code
    def getInfoFromInviteCode(self,inviteCode):
        return Guild(self.discord,self.s,self.log).getInfoFromInviteCode(inviteCode)

    #join guild with invite code
    def joinGuild(self,inviteCode):
        return Guild(self.discord,self.s,self.log).joinGuild(inviteCode)

    #kick a user
    def kick(self,guildID,userID,reason=""):
        return Guild(self.discord,self.s,self.log).kick(guildID,userID,reason)

    #ban a user
    def ban(self,guildID,userID,deleteMessagesDays=0,reason=""):
        return Guild(self.discord,self.s,self.log).ban(guildID,userID,deleteMessagesDays,reason)

    #look up a user in a guild
    def getGuildMember(self,guildID,userID):
        return Guild(self.discord,self.s,self.log).getGuildMember(guildID,userID)

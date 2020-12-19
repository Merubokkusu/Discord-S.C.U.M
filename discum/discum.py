from .start.login import *
from .start.superproperties import *

from .guild.guild import Guild
from .messages.messages import Messages
from .messages.embed import Embedder
from .user.user import User

from .gateway.gateway import *

import time
import random
import base64

class Client:
    def __init__(self, email="", password="", token="", proxy_host=None, proxy_port=None, user_agent="random", log=True):
        #vars
        self.log = log
        self.__user_token = token
        self.__user_email = email
        self.__user_password = password
        self.__proxy_host = None if proxy_host in (None,False) else proxy_host
        self.__proxy_port = None if proxy_port in (None,False) else proxy_port
        self.discord = 'https://discord.com/api/v8/'
        self.websocketurl = 'wss://gateway.discord.gg/?encoding=json&v=8&compress=zlib-stream'
        #user agent
        if user_agent != "random":
            self.__user_agent = user_agent
        else:
            import random_user_agent.user_agent #only really want to import this if needed
            self.__user_agent = random_user_agent.user_agent.UserAgent(limit=100).get_random_user_agent()
            if self.log: print('Randomly generated user agent: '+self.__user_agent)
        #headers
        self.headers = {
        	"Host": "discord.com",
        	"User-Agent": self.__user_agent,
        	"Accept": "*/*",
        	"Accept-Language": "en-US",
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
            'http': "http://" +  self.__proxy_host+':'+self.__proxy_port,
            'https': "https://" +  self.__proxy_host+':'+self.__proxy_port
            }
            self.s.proxies.update(self.proxies)
        #super-properties
        superpropertiesobj = SuperProperties(self.s, self.__user_agent, "request", self.log) #log is only used if buildnum is requested for
        self.__super_properties = superpropertiesobj.GetSuperProperties()
        self.s.headers.update({"X-Super-Properties": base64.b64encode(str(self.__super_properties).encode())})
        #token/authorization
        if self.__user_token in ("",None,False): #assuming email and pass are given...
            self.__login = Login(self.s, self.discord, self.__user_email, self.__user_password, self.log)
            self.__user_token, self.__xfingerprint = self.__login.GetToken() #update token from "" to actual value
            time.sleep(1)
        self.s.headers.update({"Authorization": self.__user_token}) #update headers
        #gateway (object initialization)
        self.gateway = GatewayServer(self.websocketurl, self.__user_token, self.__super_properties, self.__proxy_host, self.__proxy_port, self.log)

    '''
    test connection
    '''
    def connectionTest(self):
        url=self.discord+'users/@me/affinities/users'
        connection = self.s.get(url)
        if connection.status_code == 200:
            if self.log: print("Connected")
        else:
            if self.log: print("Incorrect Token")
        return connection

    '''
    discord snowflake to unix timestamp and back
    '''
    def snowflake_to_unixts(self,snowflake):
        return (snowflake/4194304+1420070400000)/1000

    def unixts_to_snowflake(self,unixts):
        return (unixts*1000-1420070400000)*4194304

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

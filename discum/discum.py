from .start.login import Login
from .start.superproperties import SuperProperties
from .start.other import Other

from .guild.guild import Guild
from .messages.messages import Messages
from .messages.embed import Embedder
from .user.user import User
from .stickers.stickers import Stickers
from .science.science import Science

from .gateway.gateway import *

import time
import base64
import requests
import random

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
        self.__super_properties = SuperProperties(self.s, buildnum="request", log=self.log).GetSuperProperties(self.__user_agent)
        self.s.headers.update({"X-Super-Properties": base64.b64encode(str(self.__super_properties).encode())})
        #token/authorization/fingerprint
        if self.__user_token in ("",None,False): #assuming email and pass are given...
            self.__user_token, self.__xfingerprint = Login(self.s, self.discord, self.log).GetToken(email, password) #update token from "" to actual value
            time.sleep(1)
        else:
            self.__xfingerprint = Login(self.s, self.discord, self.log).GetXFingerprint()
        self.s.headers.update({"Authorization": self.__user_token}) #update headers
        #gateway (object initialization)
        self.gateway = GatewayServer(self.websocketurl, self.__user_token, self.__super_properties, self.__proxy_host, self.__proxy_port, self.log)
        #embed stuff for messages
        self.Embedder = Embedder
        #get user data
        try: 
            self.userData = User(self.discord,self.s,self.log).me(with_analytics_token=True).json() #this is essentially the connection test. We need it cause we can get important data without connecting to the gateway.
            connectiontest = self.userData["analytics_token"]
        except:
            self.userData = {"analytics_token": None, "id": "0"}
        #and finally, science, which needs to be put up here because client_uuids are sequential (if you choose to use the science endpoint)
        self.Science = Science(self.discord, self.s, self.log, self.userData["analytics_token"], self.userData["id"], self.__xfingerprint)


##########################################################

    '''
    test connection
    '''
    def connectionTest(self):
        url=self.discord+'users/@me?with_analytics_token=true'
        connection = self.s.get(url)
        if connection.status_code == 200:
            if self.log: print("Connected")
            self.userData = connection.json()
        else:
            if self.log: print("Incorrect Token")
        return connection

    '''
    discord snowflake to unix timestamp and back
    '''
    def snowflake_to_unixts(self,snowflake):
        return (int(snowflake)/4194304+1420070400000)/1000

    def unixts_to_snowflake(self,unixts):
        return (int(unixts)*1000-1420070400000)*4194304

    '''
    start
    '''
    def login(self, email, password):
        return Login(self.s, self.discord, self.log).GetToken(email, password)

    def getXFingerprint(self):
        return Login(self.s, self.discord, self.log).GetXFingerprint()

    def getBuildNumber(self):
        return SuperProperties(self.s, "request", self.log).RequestBuildNumber()

    def getSuperProperties(self, user_agent, buildnum="request"):
        return SuperProperties(self.s, buildnum, self.log).GetSuperProperties(user_agent)

    def getGatewayUrl(self):
        return Other(self.s, self.discord, self.log).getGatewayUrl()

    def getDiscordStatus(self):
        return Other(self.s, self.discord, self.log).getDiscordStatus()

    def getDetectables(self):
        return Other(self.s, self.discord, self.log).getDetectables()

    def getOauth2Tokens(self):
        return Other(self.s, self.discord, self.log).getOauth2Tokens()

    def getVersionStableHash(self, underscore=None):
        return Other(self.s, self.discord, self.log).getVersionStableHash(underscore)

    '''
    Messages
    '''
    #create DM
    def createDM(self,recipients):
        return Messages(self.discord,self.s,self.log).createDM(recipients)

    #get recent messages
    def getMessages(self,channelID,num=1,beforeDate=None,aroundMessage=None): # num <= 100, beforeDate is a snowflake
        return Messages(self.discord,self.s,self.log).getMessages(channelID,num,beforeDate,aroundMessage)

    #get message by channel ID and message ID
    def getMessage(self, channelID, messageID):
        return Messages(self.discord,self.s,self.log).getMessage(channelID, messageID)

    #send messages
    def sendMessage(self, channelID, message, nonce="calculate", tts=False, embed=None, message_reference=None, allowed_mentions=None, sticker_ids=None):
        return Messages(self.discord,self.s,self.log).sendMessage(channelID, message, nonce, tts, embed, message_reference, allowed_mentions, sticker_ids)

    #send files (local or link)
    def sendFile(self,channelID,filelocation,isurl=False,message="", tts=False, message_reference=None, sticker_ids=None):
        return Messages(self.discord,self.s,self.log).sendFile(channelID,filelocation,isurl,message, tts, message_reference, sticker_ids)

    #reply, with a message and/or file
    def reply(self, channelID, messageID, message, nonce="calculate", tts=False, embed=None, allowed_mentions={"parse":["users","roles","everyone"],"replied_user":False}, sticker_ids=None, file=None, isurl=False):
        return Messages(self.discord,self.s,self.log).reply(channelID, messageID, message, nonce, tts, embed, allowed_mentions, sticker_ids, file, isurl)

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

    def bulkAck(self, data):
        return Messages(self.discord,self.s,self.log).bulkAck(data)

    def getTrendingGifs(self, provider="tenor", locale="en-US", media_format="mp4"):
        return Messages(self.discord,self.s,self.log).getTrendingGifs(provider, locale, media_format)

    '''
    Stickers
    '''
    def getStickers(self, directoryID="758482250722574376", store_listings=False, locale="en-US"):
        return Stickers(self.discord,self.s,self.log).getStickers(directoryID, store_listings, locale)

    def getStickerFile(self, stickerID, stickerAsset): #this is an animated png
        return Stickers(self.discord,self.s,self.log).getStickerFile(stickerID, stickerAsset)

    def getStickerJson(self, stickerID, stickerAsset):
        return Stickers(self.discord,self.s,self.log).getStickerJson(stickerID, stickerAsset)

    def getStickerPack(self, stickerPackID):
        return Stickers(self.discord,self.s,self.log).getStickerPack(stickerPackID)

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
    # set status
    def setStatus(self,status):
        return User(self.discord,self.s,self.log).setStatus(status)

    # set avatar
    def setAvatar(self,imagePath):
        return User(self.discord,self.s,self.log).setAvatar(imagePath)

    #set username
    def setUsername(self, username):
        return User(self.discord,self.s,self.log).setUsername(username, password=self.__user_password)

    #set email
    def setEmail(self, email):
        return User(self.discord,self.s,self.log).setEmail(email, password=self.__user_password)

    #set password
    def setPassword(self, new_password):
        return User(self.discord,self.s,self.log).setPassword(new_password, password=self.__user_password)

    #set discriminator
    def setDiscriminator(self, discriminator):
        return User(self.discord,self.s,self.log).setDiscriminator(discriminator, password=self.__user_password)

    '''
    other user stuff
    '''
    def getProfile(self, userID):
        return User(self.discord,self.s,self.log).getProfile(userID)

    def me(self, with_analytics_token=None):
        return User(self.discord,self.s,self.log).me(with_analytics_token)

    def getUserAffinities(self):
        return User(self.discord,self.s,self.log).getUserAffinities()

    def getGuildAffinities(self):
        return User(self.discord,self.s,self.log).getGuildAffinities()

    def getMentions(self, limit=25, roleMentions=True, everyoneMentions=True):
        return User(self.discord,self.s,self.log).getMentions(limit, roleMentions, everyoneMentions)

    def removeMentionFromInbox(self, messageID):
        return User(self.discord,self.s,self.log).removeMentionFromInbox(messageID)

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

    '''
    "Science", aka Discord's tracking endpoint (https://luna.gitlab.io/discord-unofficial-docs/science.html - "Discord argues that they need to collect the data in the case the User allows the usage of the data later on. Which in [luna's] opinion is complete bullshit. Have a good day.")
    '''
    def science(self, events):
        return self.Science.science(events)

    def calculateClientUUID(self, eventNum="default", userID="default", increment=True):
        return self.Science.UUIDobj.calculate(eventNum, userID, increment)

    def refreshClientUUID(self, resetEventNum=True):
        return self.Science.UUIDobj.refresh(resetEventNum)

    def parseClientUUID(self, client_uuid):
        return self.Science.UUIDobj.parse(client_uuid)

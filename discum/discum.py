from .start.login import Login
from .start.superproperties import SuperProperties
from .start.other import Other
from .start.totp import TOTP

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
    def __init__(self, email="", password="", secret="", code="", token="", proxy_host=None, proxy_port=None, user_agent="random", log=True):
        #step 1: vars
        self.log = log
        self.__user_token = token
        self.__user_email = email
        self.__user_password = password
        self.__totp_secret = secret
        self.__xfingerprint = ""
        self.userData = {}
        self.__proxy_host = None if proxy_host in (None,False) else proxy_host
        self.__proxy_port = None if proxy_port in (None,False) else proxy_port
        self.discord = 'https://discord.com/api/v8/'
        self.websocketurl = 'wss://gateway.discord.gg/?encoding=json&v=8&compress=zlib-stream'
        #step 2: user agent
        if user_agent != "random":
            self.__user_agent = user_agent
        else:
            import random_user_agent.user_agent #only really want to import this if needed
            self.__user_agent = random_user_agent.user_agent.UserAgent(limit=100).get_random_user_agent()
            if self.log: print('Randomly generated user agent: '+self.__user_agent)
        #step 3: http request headers
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
        #step 4: super-properties (part of headers)
        self.__super_properties = SuperProperties(self.s, buildnum="request", log=self.log).GetSuperProperties(self.__user_agent)
        self.s.headers.update({"X-Super-Properties": base64.b64encode(str(self.__super_properties).encode())})
        #step 5: token/authorization/fingerprint (also part of headers, except for fingerprint)
        if self.__user_token in ("",None,False): #assuming email and pass are given...
            self.__user_token, self.__xfingerprint = Login(self.s, self.discord, self.log).GetToken(email=email, password=password, secret=secret, code=code) #update token from "" to actual value
            time.sleep(1)            
        self.s.headers.update({"Authorization": self.__user_token}) #update headers
        #step 6: gateway (object initialization)
        self.gateway = GatewayServer(self.websocketurl, self.__user_token, self.__super_properties, self.__proxy_host, self.__proxy_port, self.log)
        #step 7: embed (object initialization)
        self.Embedder = Embedder
        #step 8: somewhat prepare for science events
        self.Science = ""

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
    def login(self, email, password, undelete=False, captcha=None, source=None, gift_code_sku_id=None, secret="", code=""):
        return Login(self.s, self.discord, self.log).GetToken(email, password, undelete, captcha, source, gift_code_sku_id, secret, code)

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
    def setUsername(self, username): #USER PASSWORD NEEDS TO BE SET BEFORE THIS IS RUN
        return User(self.discord,self.s,self.log).setUsername(username, password=self.__user_password)

    #set email
    def setEmail(self, email): #USER PASSWORD NEEDS TO BE SET BEFORE THIS IS RUN
        return User(self.discord,self.s,self.log).setEmail(email, password=self.__user_password)

    #set password
    def setPassword(self, new_password): #USER PASSWORD NEEDS TO BE SET BEFORE THIS IS RUN
        return User(self.discord,self.s,self.log).setPassword(new_password, password=self.__user_password)

    #set discriminator
    def setDiscriminator(self, discriminator): #USER PASSWORD NEEDS TO BE SET BEFORE THIS IS RUN
        return User(self.discord,self.s,self.log).setDiscriminator(discriminator, password=self.__user_password)

    '''
    other user stuff
    '''
    def getProfile(self, userID):
        return User(self.discord,self.s,self.log).getProfile(userID)

    def info(self, with_analytics_token=None):
        return User(self.discord,self.s,self.log).info(with_analytics_token)

    def getUserAffinities(self):
        return User(self.discord,self.s,self.log).getUserAffinities()

    def getGuildAffinities(self):
        return User(self.discord,self.s,self.log).getGuildAffinities()

    def getMentions(self, limit=25, roleMentions=True, everyoneMentions=True):
        return User(self.discord,self.s,self.log).getMentions(limit, roleMentions, everyoneMentions)

    def removeMentionFromInbox(self, messageID):
        return User(self.discord,self.s,self.log).removeMentionFromInbox(messageID)

    def setHypesquad(self, house):
        return User(self.discord,self.s,self.log).setHypesquad(house)

    def leaveHypesquad(self):
        return User(self.discord,self.s,self.log).leaveHypesquad()

    def setLocale(self, locale):
        return User(self.discord,self.s,self.log).setLocale(locale)

    def calculateTOTPcode(self, secret="default"): #need to put this function here (instead of in login folder or user folder) because it updates the secret (if and only if secret == "")
        if secret == "default":
            if self.__totp_secret == "":
                self.__totp_secret = ''.join(random.choice(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ234567')) for _ in range(16)) #random base32 (len 16)
            secret = self.__totp_secret
        if "?secret=" in secret:
            secret = secret[secret.index("?secret=")+8: secret.index("?secret=")+24]
        return TOTP(secret).generateTOTP(), secret #secret is returned just in case it wasn't set at the beginning.

    def getTOTPurl(self, secret): #use this to store your totp secret/qr pic; btw url format is otpauth://totp/Discord:EMAIL?secret=SECRET&issuer=Discord
        url = "otpauth://totp/Discord"
        if self.__user_email != "":
            url += ":"+self.__user_email
        url += "?secret="+secret+"&issuer=Discord"
        return url

    def enable2FA(self): #this also returns backup codes (value of key "backup_codes"). USER PASSWORD NEEDS TO BE SET BEFORE THIS IS RUN
        code = self.calculateTOTPcode()[0]
        result = User(self.discord,self.s,self.log).enable2FA(code, secret=self.__totp_secret, password=self.__user_password)
        self.__user_token = result.json()["token"]
        self.s.headers['Authorization'] = self.__user_token
        return result

    def disable2FA(self, code="calculate", clearSecretAfter=False): #either set your token before running this or input a code.
        if code == "calculate":
            code = self.calculateTOTPcode()[0] #this will generate a random secret if you dont have one set, so...set your secret before running this
        code = str(code) #just in case
        result = User(self.discord,self.s,self.log).disable2FA(code)
        self.__user_token = result.json()["token"]
        self.s.headers['Authorization'] = self.__user_token
        if clearSecretAfter: #this is dangerous (even though disable2FA should error out before getting to this point if something goes wrong). If you already have your secret saved, clear away. By default this is set to False to avoid any mishaps.
            self.__totp_secret = ""
        return result

    def getRTCregions(self):
        return User(self.discord,self.s,self.log).getRTCregions()

    def setAFKtimeout(self, timeout_seconds):
        return User(self.discord,self.s,self.log).setAFKtimeout(timeout_seconds)

    def setTheme(self, theme): #"light" or "dark"
        return User(self.discord,self.s,self.log).setTheme(theme)

    def setMessageDisplay(self, CozyOrCompact): #"cozy" or "compact"
        return User(self.discord,self.s,self.log).setMessageDisplay(CozyOrCompact)

    def enableDevMode(self, enable): #boolean, default=False
        return User(self.discord,self.s,self.log).enableDevMode(enable)

    def activateApplicationTestMode(self, applicationID):
        return User(self.discord,self.s,self.log).activateApplicationTestMode(applicationID)

    def getApplicationData(self, applicationID, with_guild=False):
        return User(self.discord,self.s,self.log).getApplicationData(applicationID, with_guild)

    def getBackupCodes(self, regenerate=False):
        return User(self.discord,self.s,self.log).getBackupCodes(self.__user_password, regenerate)

    def enableInlineMedia(self, enable): #boolean, default=True
        return User(self.discord,self.s,self.log).enableInlineMedia(enable)

    def enableLargeImagePreview(self, enable): #boolean, default=True
        return User(self.discord,self.s,self.log).enableLargeImagePreview(enable)

    def enableGifAutoPlay(self, enable): #boolean, default=True
        return User(self.discord,self.s,self.log).enableGifAutoPlay(enable)

    def enableLinkPreview(self, enable): #boolean, default=True
        return User(self.discord,self.s,self.log).enableLinkPreview(enable)

    def enableReactionRendering(self, enable): #boolean, default=True
        return User(self.discord,self.s,self.log).enableReactionRendering(enable)

    def enableAnimatedEmoji(self, enable): #boolean, default=True
        return User(self.discord,self.s,self.log).enableAnimatedEmoji(enable)

    def enableEmoticonConversion(self, enable): #boolean, default=True
        return User(self.discord,self.s,self.log).enableEmoticonConversion(enable)

    def stickerAnimation(self, setting): #string, default="always"
        return User(self.discord,self.s,self.log).stickerAnimation(setting)

    def enableTTS(self, enable): #boolean, default=True
        return User(self.discord,self.s,self.log).enableTTS(enable)

    def getBillingHistory(self, limit=20):
        return User(self.discord,self.s,self.log).getBillingHistory(limit)

    def getPaymentSources(self):
        return User(self.discord,self.s,self.log).getPaymentSources()

    def getBillingSubscriptions(self):
        return User(self.discord,self.s,self.log).getBillingSubscriptions()

    def getStripeClientSecret(self):
        return User(self.discord,self.s,self.log).getStripeClientSecret()

    def logout(self, provider=None, voip_provider=None):
        return User(self.discord,self.s,self.log).logout(provider, voip_provider)

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

    def getMemberVerificationData(self, guildID, with_guild=False, invite_code=None):
        return Guild(self.discord,self.s,self.log).getMemberVerificationData(guildID, with_guild, invite_code)

    def agreeGuildRules(self, guildID, form_fields, version="2021-01-05T01:44:32.163000+00:00"):
        return Guild(self.discord,self.s,self.log).agreeGuildRules(guildID, form_fields, version)

    '''
    "Science", aka Discord's tracking endpoint (https://luna.gitlab.io/discord-unofficial-docs/science.html - "Discord argues that they need to collect the data in the case the User allows the usage of the data later on. Which in [luna's] opinion is complete bullshit. Have a good day.")
    '''
    def science(self, events): #the real prep for science events happens down here, and only once for each client obj
        if self.Science == "":
            try:
                #get xfingerprint
                if self.__xfingerprint == "":
                    self.__xfingerprint = Login(self.s, self.discord, self.log).GetXFingerprint()
                    time.sleep(1)
                #get analytics token
                self.userData = User(self.discord,self.s,self.log).info(with_analytics_token=True).json() #this is essentially the connection test. We need it cause we can get important data without connecting to the gateway.
                connectiontest = self.userData["analytics_token"]
            except:
                self.userData = {"analytics_token": None, "id": "0"} #if token invalid
            #initialize Science object
            self.Science = Science(self.discord, self.s, self.log, self.userData["analytics_token"], self.userData["id"], self.__xfingerprint)
        return self.Science.science(events)

    def calculateClientUUID(self, eventNum="default", userID="default", increment=True):
        return self.Science.UUIDobj.calculate(eventNum, userID, increment)

    def refreshClientUUID(self, resetEventNum=True):
        return self.Science.UUIDobj.refresh(resetEventNum)

    def parseClientUUID(self, client_uuid):
        return self.Science.UUIDobj.parse(client_uuid)

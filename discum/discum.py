#to speed up importing discum & only import modules when they are needed
from .importmanager import Imports
imports = Imports(
	{
		"Wrapper": "discum.RESTapiwrap",
		"Login": "discum.start.login",
		"SuperProperties": "discum.start.superproperties",
		"Other": "discum.start.other",
		"Guild": "discum.guild.guild",
		"Messages": "discum.messages.messages",
		"User": "discum.user.user",
		"Stickers": "discum.stickers.stickers",
		"Science": "discum.science.science",
		"TOTP": "discum.utils.totp",
		"RemoteAuth": "discum.gateway.remoteauth",
		"SlashCommands": "discum.interactions.slashcommands",
		"Buttons": "discum.interactions.buttons"
	}
)

#logging to console/file
from .logger import * #imports LogLevel and Logger

#other imports
import time
import base64
import json
import requests
import random

#client initialization
class Client:
	__slots__ = ['log', 'locale', '__user_token', '__user_email', '__user_password', '__totp_secret', '__xfingerprint', 'userData', '__proxy_host', '__proxy_port', 'api_version', 'discord', 'websocketurl', 'remoteauthurl', '__user_agent', 's', '__super_properties', 'gateway', 'Science']
	def __init__(self, email="", password="", secret="", code="", token="", remote_auth=False, proxy_host=None, proxy_port=None, user_agent="random", locale="en-US", build_num="request", log={"console":True, "file":False}):
		#step 1: vars
		self.log = log
		self.locale = locale
		self.__user_token = token
		self.__user_email = email
		self.__user_password = password
		self.__totp_secret = secret
		self.__xfingerprint = ""
		self.userData = {} #used if science requests are used
		self.__proxy_host = None if proxy_host in (None,False) else proxy_host
		self.__proxy_port = None if proxy_port in (None,False) else proxy_port
		self.api_version = 9
		self.discord = 'https://discord.com/api/v'+repr(self.api_version)+'/'
		self.websocketurl = 'wss://gateway.discord.gg/?encoding=json&v='+repr(self.api_version)+'&compress=zlib-stream'
		self.remoteauthurl = 'wss://remote-auth-gateway.discord.gg/?v=1'
		#step 2: user agent
		if user_agent != "random":
			self.__user_agent = user_agent
		else:
			import random_user_agent.user_agent #only really want to import this if needed
			self.__user_agent = random_user_agent.user_agent.UserAgent(limit=100).get_random_user_agent()
			Logger.log('Randomly generated user agent: '+self.__user_agent, None, log)
		#step 3: http request headers
		headers = {
			"Origin": "https://discord.com",
			"User-Agent": self.__user_agent,
			"Accept": "*/*",
			"Accept-Encoding": "gzip, deflate, br",
			"Accept-Language": self.locale,
			"Cache-Control": "no-cache",
			"Pragma": "no-cache",
			"Referer": "https://discord.com/channels/@me",
			"Sec-Fetch-Dest": "empty",
			"Sec-Fetch-Mode": "cors",
			"Sec-Fetch-Site": "same-origin",
			"Connection": "keep-alive",
			"Content-Type": "application/json"
		}
		self.s = requests.Session()
		self.s.headers.update(headers)
		if self.__proxy_host != None: #self.s.proxies defaults to {}
			proxies = {
			'http': "http://" + self.__proxy_host+':'+self.__proxy_port,
			'https': "https://" + self.__proxy_host+':'+self.__proxy_port
			}
			self.s.proxies.update(proxies)
		#step 4: cookies
		self.s.cookies.update({"locale": self.locale})
		#step 5: super-properties (part of headers)
		self.__super_properties = imports.SuperProperties(self.s, buildnum=build_num, log=self.log).getSuperProperties(self.__user_agent, self.locale)
		self.s.headers.update({"X-Super-Properties": base64.b64encode(json.dumps(self.__super_properties).encode()).decode("utf-8")})
		#step 6: token/authorization/fingerprint (also part of headers, except for fingerprint)
		tokenProvided = self.__user_token not in ("",None,False)
		if not tokenProvided:
			if remote_auth:
				self.__user_token, self.userData = self.remoteAuthLogin(remote_auth)
			else:
				loginResponse, self.__xfingerprint = imports.Login(self.s, self.discord, self.log).login(email=email, password=password, undelete=False, captcha=None, source=None, gift_code_sku_id=None, secret=secret, code=code)
				self.__user_token = loginResponse.json().get('token') #update token from "" to actual value
				time.sleep(1)
		self.s.headers.update({"Authorization": self.__user_token}) #update headers
		#step 7: gateway (object initialization)
		from .gateway.gateway import GatewayServer
		self.gateway = GatewayServer(self.websocketurl, self.__user_token, self.__super_properties, self.s, self.discord, self.log) #self.s contains proxy host and proxy port already
		#step 8: somewhat prepare for science events
		self.Science = ""

##########################################################

	'''
	test token
	'''
	def checkToken(self, token):
		editedS = imports.Wrapper().editedReqSession(self.s, {"update":{"Authorization":token}})
		connection = imports.User(self.discord, editedS, self.log).info(with_analytics_token=True)
		if connection.status_code == 200:
			Logger.log("Valid token.", None, self.log)
		else:
			Logger.log("Invalid token.", None, self.log)
		return connection

	'''
	discord snowflake to unix timestamp and back
	'''
	def snowflake_to_unixts(self,snowflake):
		return (int(float(snowflake))/4194304+1420070400000)/1000

	def unixts_to_snowflake(self,unixts):
		return (int(float(unixts))*1000-1420070400000)*4194304

	'''
	start
	'''
	def login(self, email, password, undelete=False, captcha=None, source=None, gift_code_sku_id=None, secret="", code=""):
		return imports.Login(self.s, self.discord, self.log).login(email, password, undelete, captcha, source, gift_code_sku_id, secret, code)

	def getXFingerprint(self):
		return imports.Login(self.s, self.discord, self.log).getXFingerprint()

	def getBuildNumber(self):
		return imports.SuperProperties(self.s, "request", self.log).requestBuildNumber()

	def getSuperProperties(self, user_agent, buildnum="request", locale=None):
		return imports.SuperProperties(self.s, buildnum, self.log).getSuperProperties(user_agent, locale) #self.locale

	def getGatewayUrl(self):
		return imports.Other(self.s, self.discord, self.log).getGatewayUrl()

	def getDiscordStatus(self):
		return imports.Other(self.s, self.discord, self.log).getDiscordStatus()

	def getDetectables(self):
		return imports.Other(self.s, self.discord, self.log).getDetectables()

	def getOauth2Tokens(self):
		return imports.Other(self.s, self.discord, self.log).getOauth2Tokens()

	def getVersionStableHash(self, underscore=None):
		return imports.Other(self.s, self.discord, self.log).getVersionStableHash(underscore)

	def initRA(self):
		self.ra = imports.RemoteAuth(self.remoteauthurl, self.__user_agent, self.__proxy_host, self.__proxy_port, self.log)

	def remoteAuthLogin(self, saveQrCode=True):
		self.initRA()
		return self.ra.run(saveQrCode)

	'''
	Messages
	'''
	#create DM
	def createDM(self,recipients):
		return imports.Messages(self.discord,self.s,self.log).createDM(recipients)

	#delete channel/DM/DM group
	def deleteChannel(self, channelID):
		return imports.Messages(self.discord,self.s,self.log).deleteChannel(channelID)

	#remove from DM group
	def removeFromDmGroup(self, channelID, userID):
		return imports.Messages(self.discord,self.s,self.log).removeFromDmGroup(channelID, userID)

	#add to DM group
	def addToDmGroup(self, channelID, userID):
		return imports.Messages(self.discord,self.s,self.log).addToDmGroup(channelID, userID)

	#create DM group invite link
	def createDmGroupInvite(self, channelID, max_age_seconds=86400):
		return imports.Messages(self.discord,self.s,self.log).createDmGroupInvite(channelID, max_age_seconds)

	#change DM group name
	def setDmGroupName(self, channelID, name):
		return imports.Messages(self.discord,self.s,self.log).setDmGroupName(channelID, name)

	#change DM icon
	def setDmGroupIcon(self, channelID, imagePath):
		return imports.Messages(self.discord,self.s,self.log).setDmGroupIcon(channelID, imagePath)

	#get recent messages
	def getMessages(self,channelID,num=1,beforeDate=None,aroundMessage=None): # num <= 100, beforeDate is a snowflake
		return imports.Messages(self.discord,self.s,self.log).getMessages(channelID,num,beforeDate,aroundMessage)

	#get message by channel ID and message ID
	def getMessage(self, channelID, messageID):
		return imports.Messages(self.discord,self.s,self.log).getMessage(channelID, messageID)

	#greet with stickers
	def greet(self, channelID, sticker_ids=["749054660769218631"]):
		return imports.Messages(self.discord,self.s,self.log).greet(channelID, sticker_ids)

	#send messages
	def sendMessage(self, channelID, message, nonce="calculate", tts=False, embed=None, message_reference=None, allowed_mentions=None, sticker_ids=None):
		return imports.Messages(self.discord,self.s,self.log).sendMessage(channelID, message, nonce, tts, embed, message_reference, allowed_mentions, sticker_ids)

	#send files (local or link)
	def sendFile(self,channelID,filelocation,isurl=False,message="", tts=False, message_reference=None, sticker_ids=None):
		return imports.Messages(self.discord,self.s,self.log).sendFile(channelID,filelocation,isurl,message, tts, message_reference, sticker_ids)

	#reply, with a message and/or file
	def reply(self, channelID, messageID, message, nonce="calculate", tts=False, embed=None, allowed_mentions={"parse":["users","roles","everyone"],"replied_user":False}, sticker_ids=None, file=None, isurl=False):
		return imports.Messages(self.discord,self.s,self.log).reply(channelID, messageID, message, nonce, tts, embed, allowed_mentions, sticker_ids, file, isurl)

	#search messages
	def searchMessages(self, guildID, channelID=None, authorID=None, authorType=None, mentionsUserID=None, has=None, linkHostname=None, embedProvider=None, embedType=None, attachmentExtension=None, attachmentFilename=None, mentionsEveryone=None, includeNsfw=None, afterDate=None, beforeDate=None, textSearch=None, afterNumResults=None, limit=None):
		return imports.Messages(self.discord,self.s,self.log).searchMessages(guildID, channelID, authorID, authorType, mentionsUserID, has, linkHostname, embedProvider, embedType, attachmentExtension, attachmentFilename, mentionsEveryone, includeNsfw, afterDate, beforeDate, textSearch, afterNumResults, limit)

	#filter searchMessages, takes in the output of searchMessages (a requests response object) and outputs a list of target messages
	def filterSearchResults(self,searchResponse):
		return imports.Messages(self.discord,self.s,self.log).filterSearchResults(searchResponse)

	#sends the typing action for 10 seconds (or technically until you change the page)
	def typingAction(self,channelID):
		return imports.Messages(self.discord,self.s,self.log).typingAction(channelID)

	#delete message
	def deleteMessage(self,channelID,messageID):
		return imports.Messages(self.discord,self.s,self.log).deleteMessage(channelID,messageID)

	#edit message
	def editMessage(self,channelID,messageID,newMessage):
		return imports.Messages(self.discord,self.s,self.log).editMessage(channelID, messageID, newMessage)

	#pin message
	def pinMessage(self,channelID,messageID):
		return imports.Messages(self.discord,self.s,self.log).pinMessage(channelID,messageID)

	#un-pin message
	def unPinMessage(self,channelID,messageID):
		return imports.Messages(self.discord,self.s,self.log).unPinMessage(channelID,messageID)

	#get pinned messages
	def getPins(self,channelID):
		return imports.Messages(self.discord,self.s,self.log).getPins(channelID)

	#add reaction
	def addReaction(self,channelID,messageID,emoji):
		return imports.Messages(self.discord,self.s,self.log).addReaction(channelID,messageID,emoji)

	#remove reaction
	def removeReaction(self,channelID,messageID,emoji):
		return imports.Messages(self.discord,self.s,self.log).removeReaction(channelID,messageID,emoji)

	#acknowledge message (mark message read)
	def ackMessage(self,channelID,messageID,ackToken=None):
		return imports.Messages(self.discord,self.s,self.log).ackMessage(channelID,messageID,ackToken)

	#unacknowledge message (mark message unread)
	def unAckMessage(self,channelID,messageID,numMentions=0):
		return imports.Messages(self.discord,self.s,self.log).unAckMessage(channelID,messageID,numMentions)

	def bulkAck(self, data):
		return imports.Messages(self.discord,self.s,self.log).bulkAck(data)

	def getTrendingGifs(self, provider="tenor", locale="en-US", media_format="mp4"):
		return imports.Messages(self.discord,self.s,self.log).getTrendingGifs(provider, locale, media_format)

	'''
	Stickers
	'''
	def getStickers(self, directoryID="758482250722574376", store_listings=False, locale="en-US"):
		return imports.Stickers(self.discord,self.s,self.log).getStickers(directoryID, store_listings, locale)

	def getStickerFile(self, stickerID, stickerAsset): #this is an animated png
		return imports.Stickers(self.discord,self.s,self.log).getStickerFile(stickerID, stickerAsset)

	def getStickerJson(self, stickerID, stickerAsset):
		return imports.Stickers(self.discord,self.s,self.log).getStickerJson(stickerID, stickerAsset)

	def getStickerPack(self, stickerPackID):
		return imports.Stickers(self.discord,self.s,self.log).getStickerPack(stickerPackID)

	'''
	User relationships
	'''
	#get relationships
	def getRelationships(self):
		return imports.User(self.discord,self.s,self.log).getRelationships()

	#create outgoing friend request
	def requestFriend(self, user): #you can input a userID(snowflake) or a user discriminator
		return imports.User(self.discord,self.s,self.log).requestFriend(user)

	#accept incoming friend request
	def acceptFriend(self, userID, location="friends"):
		return imports.User(self.discord,self.s,self.log).acceptFriend(userID, location)

	#remove friend OR unblock user
	def removeRelationship(self, userID, location="context menu"):
		return imports.User(self.discord,self.s,self.log).removeRelationship(userID, location)

	#block user
	def blockUser(self, userID, location="context menu"):
		return imports.User(self.discord,self.s,self.log).blockUser(userID, location)

	'''
	Other user stuff
	'''
	def getProfile(self, userID, with_mutual_guilds=True):
		return imports.User(self.discord,self.s,self.log).getProfile(userID, with_mutual_guilds)

	def info(self, with_analytics_token=None):
		return imports.User(self.discord,self.s,self.log).info(with_analytics_token)

	def getUserAffinities(self):
		return imports.User(self.discord,self.s,self.log).getUserAffinities()

	def getGuildAffinities(self):
		return imports.User(self.discord,self.s,self.log).getGuildAffinities()

	def getMentions(self, limit=25, roleMentions=True, everyoneMentions=True):
		return imports.User(self.discord,self.s,self.log).getMentions(limit, roleMentions, everyoneMentions)

	def removeMentionFromInbox(self, messageID):
		return imports.User(self.discord,self.s,self.log).removeMentionFromInbox(messageID)

	def getMyStickers(self):
		return imports.User(self.discord,self.s,self.log).getMyStickers()

	def getNotes(self, userID):
		return imports.User(self.discord,self.s,self.log).getNotes(userID)

	def setUserNote(self, userID, note):
		return imports.User(self.discord,self.s,self.log).setUserNote(userID, note)

	def getRTCregions(self):
		return imports.User(self.discord,self.s,self.log).getRTCregions()

	'''
	Profile edits
	'''
	# set avatar
	def setAvatar(self,imagePath):
		return imports.User(self.discord,self.s,self.log).setAvatar(imagePath)

	#set profile color
	def setProfileColor(self, color=None):
		return imports.User(self.discord,self.s,self.log).setProfileColor(color)

	#set username
	def setUsername(self, username): #USER PASSWORD NEEDS TO BE SET BEFORE THIS IS RUN
		return imports.User(self.discord,self.s,self.log).setUsername(username, password=self.__user_password)

	#set email
	def setEmail(self, email): #USER PASSWORD NEEDS TO BE SET BEFORE THIS IS RUN
		return imports.User(self.discord,self.s,self.log).setEmail(email, password=self.__user_password)

	#set password
	def setPassword(self, new_password): #USER PASSWORD NEEDS TO BE SET BEFORE THIS IS RUN
		return imports.User(self.discord,self.s,self.log).setPassword(new_password, password=self.__user_password)

	#set discriminator
	def setDiscriminator(self, discriminator): #USER PASSWORD NEEDS TO BE SET BEFORE THIS IS RUN
		return imports.User(self.discord,self.s,self.log).setDiscriminator(discriminator, password=self.__user_password)

	#set about me
	def setAboutMe(self, bio):
		return imports.User(self.discord,self.s,self.log).setAboutMe(bio)

	#set banner
	def setBanner(self, imagePath):
		return imports.User(self.discord,self.s,self.log).setBanner(imagePath)

	#2FA
	def calculateTOTPcode(self, secret="default"): #need to put this function here (instead of in login folder or user folder) because it updates the secret (if and only if secret == "")
		if secret == "default":
			if self.__totp_secret == "":
				self.__totp_secret = ''.join(random.choice(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ234567')) for _ in range(16)) #random base32 (len 16)
			secret = self.__totp_secret
		if "?secret=" in secret:
			secret = secret[secret.index("?secret=")+8: secret.index("?secret=")+24]
		return imports.TOTP(secret).generateTOTP(), secret #secret is returned just in case it wasn't set at the beginning.

	def getTOTPurl(self, secret): #use this to store your totp secret/qr pic; btw url format is otpauth://totp/Discord:EMAIL?secret=SECRET&issuer=Discord
		url = "otpauth://totp/Discord"
		if self.__user_email != "":
			url += ":"+self.__user_email
		url += "?secret="+secret+"&issuer=Discord"
		return url

	def enable2FA(self): #this also returns backup codes (value of key "backup_codes"). USER PASSWORD NEEDS TO BE SET BEFORE THIS IS RUN
		code = self.calculateTOTPcode()[0]
		result = imports.User(self.discord,self.s,self.log).enable2FA(code, secret=self.__totp_secret, password=self.__user_password)
		self.__user_token = result.json()["token"]
		self.s.headers['Authorization'] = self.__user_token
		return result

	def disable2FA(self, code="calculate", clearSecretAfter=False): #either set your token before running this or input a code.
		if code == "calculate":
			code = self.calculateTOTPcode()[0] #this will generate a random secret if you dont have one set, so...set your secret before running this
		code = str(code) #just in case
		result = imports.User(self.discord,self.s,self.log).disable2FA(code)
		self.__user_token = result.json()["token"]
		self.s.headers['Authorization'] = self.__user_token
		if clearSecretAfter: #this is dangerous (even though disable2FA should error out before getting to this point if something goes wrong). If you already have your secret saved, clear away. By default this is set to False to avoid any mishaps.
			self.__totp_secret = ""
		return result

	def getBackupCodes(self, regenerate=False):
		return imports.User(self.discord,self.s,self.log).getBackupCodes(self.__user_password, regenerate)

	def disableAccount(self, password):
		return imports.User(self.discord,self.s,self.log).disableAccount(password)

	def deleteAccount(self, password):
		return imports.User(self.discord,self.s,self.log).deleteAccount(password)

	def setPhone(self, number):
		return imports.User(self.discord,self.s,self.log).setPhone(number)

	def validatePhone(self, number, code):
		result = imports.User(self.discord,self.s,self.log).validatePhone(number, code)
		if result.status_code == 200 and "token" in result.json():
			self.__user_token = result.json()["token"]
		return result

	'''
	User Settings, continued
	'''
	def setDMscanLvl(self, level=1): # 0<=level<=2
		return imports.User(self.discord,self.s,self.log).setDMscanLvl(level)

	def allowDMsFromServerMembers(self, allow=True, disallowedGuildIDs=None):
		return imports.User(self.discord,self.s,self.log).allowDMsFromServerMembers(allow, disallowedGuildIDs)

	def allowFriendRequestsFrom(self, types=["everyone", "mutual_friends", "mutual_guilds"]):
		return imports.User(self.discord,self.s,self.log).allowFriendRequestsFrom(types)

	def analyticsConsent(self, grant=[], revoke=[]):
		return imports.User(self.discord,self.s,self.log).analyticsConsent(grant, revoke)

	def allowScreenReaderTracking(self, allow=True):
		return imports.User(self.discord,self.s,self.log).allowScreenReaderTracking(allow)

	def requestMyData(self):
		return imports.User(self.discord,self.s,self.log).requestMyData()

	def getConnectedAccounts(self):
		return imports.User(self.discord,self.s,self.log).getConnectedAccounts()

	def getConnectionUrl(self, accountType):
		return imports.User(self.discord,self.s,self.log).getConnectionUrl(accountType)

	def enableConnectionDisplayOnProfile(self, accountType, accountUsername, enable=True):
		return imports.User(self.discord,self.s,self.log).enableConnectionDisplayOnProfile(accountType, accountUsername, enable)

	def enableConnectionDisplayOnStatus(self, accountType, accountUsername, enable=True):
		return imports.User(self.discord,self.s,self.log).enableConnectionDisplayOnStatus(accountType, accountUsername, enable)

	def removeConnection(self, accountType, accountUsername):
		return imports.User(self.discord,self.s,self.log).removeConnection(accountType, accountUsername)

	def getBillingHistory(self, limit=20):
		return imports.User(self.discord,self.s,self.log).getBillingHistory(limit)

	def getPaymentSources(self):
		return imports.User(self.discord,self.s,self.log).getPaymentSources()

	def getBillingSubscriptions(self):
		return imports.User(self.discord,self.s,self.log).getBillingSubscriptions()

	def getStripeClientSecret(self):
		return imports.User(self.discord,self.s,self.log).getStripeClientSecret()

	def setTheme(self, theme): #"light" or "dark"
		return imports.User(self.discord,self.s,self.log).setTheme(theme)

	def setMessageDisplay(self, CozyOrCompact): #"cozy" or "compact"
		return imports.User(self.discord,self.s,self.log).setMessageDisplay(CozyOrCompact)

	def enableGifAutoPlay(self, enable=True): #boolean, default=True
		return imports.User(self.discord,self.s,self.log).enableGifAutoPlay(enable)

	def enableAnimatedEmoji(self, enable=True): #boolean, default=True
		return imports.User(self.discord,self.s,self.log).enableAnimatedEmoji(enable)

	def setStickerAnimation(self, setting): #string, default="always"
		return imports.User(self.discord,self.s,self.log).setStickerAnimation(setting)

	def enableTTS(self, enable=True): #boolean, default=True
		return imports.User(self.discord,self.s,self.log).enableTTS(enable)

	def enableLinkedImageDisplay(self, enable=True): #boolean, default=True
		return imports.User(self.discord,self.s,self.log).enableLinkedImageDisplay(enable)

	def enableImageDisplay(self, enable=True): #boolean, default=True
		return imports.User(self.discord,self.s,self.log).enableImageDisplay(enable)

	def enableLinkPreview(self, enable=True): #boolean, default=True
		return imports.User(self.discord,self.s,self.log).enableLinkPreview(enable)

	def enableReactionRendering(self, enable=True): #boolean, default=True
		return imports.User(self.discord,self.s,self.log).enableReactionRendering(enable)

	def enableEmoticonConversion(self, enable=True): #boolean, default=True
		return imports.User(self.discord,self.s,self.log).enableEmoticonConversion(enable)

	def setAFKtimeout(self, timeout_seconds):
		return imports.User(self.discord,self.s,self.log).setAFKtimeout(timeout_seconds)

	def setLocale(self, locale):
		response = imports.User(self.discord,self.s,self.log).setLocale(locale)
		self.locale = locale
		self.s.headers["Accept-Language"] = self.locale
		self.s.cookies["locale"] = self.locale
		return response

	def enableDevMode(self, enable=True): #boolean
		return imports.User(self.discord,self.s,self.log).enableDevMode(enable)

	def activateApplicationTestMode(self, applicationID):
		return imports.User(self.discord,self.s,self.log).activateApplicationTestMode(applicationID)

	def getApplicationData(self, applicationID, with_guild=False):
		return imports.User(self.discord,self.s,self.log).getApplicationData(applicationID, with_guild)

	def enableActivityDisplay(self, enable=True):
		return imports.User(self.discord,self.s,self.log).enableActivityDisplay(enable)

	def setHypesquad(self, house):
		return imports.User(self.discord,self.s,self.log).setHypesquad(house)

	def leaveHypesquad(self):
		return imports.User(self.discord,self.s,self.log).leaveHypesquad()

	def getBuildOverrides(self):
		return imports.User(self.discord,self.s,self.log).getBuildOverrides()

	def enableSourceMaps(self, enable=True):
		return imports.User(self.discord,self.s,self.log).enableSourceMaps()

	def suppressEveryonePings(self, guildID, suppress=True):
		return imports.User(self.discord,self.s,self.log).suppressEveryonePings(guildID, suppress)

	def suppressRoleMentions(self, guildID, suppress=True):
		return imports.User(self.discord,self.s,self.log).suppressRoleMentions(guildID, suppress)

	def enableMobilePushNotifications(self, guildID, enable=True):
		return imports.User(self.discord,self.s,self.log).enableMobilePushNotifications(guildID, enable)

	def setChannelNotificationOverrides(self, guildID, overrides):
		return imports.User(self.discord,self.s,self.log).setChannelNotificationOverrides(guildID, overrides)

	def setMessageNotifications(self, guildID, notifications):
		return imports.User(self.discord,self.s,self.log).setMessageNotifications(guildID, notifications)

	def muteGuild(self, guildID, mute=True, duration=None):
		return imports.User(self.discord,self.s,self.log).muteGuild(guildID, mute, duration)

	def muteDM(self, DMID, mute=True, duration=None):
		return imports.User(self.discord,self.s,self.log).muteDM(DMID, mute, duration)

	def setThreadNotifications(self, threadID, notifications):
		return imports.User(self.discord,self.s,self.log).setThreadNotifications(threadID, notifications)

	def getReportMenu(self):
		return imports.User(self.discord,self.s,self.log).getReportMenu()

	def reportSpam(self, channelID, messageID, reportType="first_dm", guildID=None, version="1.0", variant="1", language="en"):
		return imports.User(self.discord,self.s,self.log).reportSpam(channelID, messageID, reportType, guildID, version, variant, language)

	def logout(self, provider=None, voip_provider=None):
		return imports.User(self.discord,self.s,self.log).logout(provider, voip_provider)

	'''
	Guild/Server stuff
	'''
	#get guild info from invite code
	def getInfoFromInviteCode(self,inviteCode, with_counts=True, with_expiration=True, fromJoinGuildNav=False):
		return imports.Guild(self.discord,self.s,self.log).getInfoFromInviteCode(inviteCode, with_counts, with_expiration, fromJoinGuildNav)

	#join guild with invite code
	def joinGuild(self, inviteCode, location="accept invite page", wait=0):
		return imports.Guild(self.discord,self.s,self.log).joinGuild(inviteCode, location, wait)

	#preview/lurk-join guild. Only applies to current (gateway) session
	def previewGuild(self, guildID, sessionID=None):
		return imports.Guild(self.discord,self.s,self.log).previewGuild(guildID, sessionID)

	#leave guild
	def leaveGuild(self, guildID, lurking=False):
		return imports.Guild(self.discord,self.s,self.log).leaveGuild(guildID, lurking)

	#create invite
	def createInvite(self, channelID, max_age_seconds=False, max_uses=False, grantTempMembership=False, checkInvite="", targetType=""):
		return imports.Guild(self.discord,self.s,self.log).createInvite(channelID, max_age_seconds, max_uses, grantTempMembership, checkInvite, targetType)

	def deleteInvite(self, inviteCode):
		return imports.Guild(self.discord,self.s,self.log).deleteInvite(inviteCode)

	def getGuildInvites(self, guildID):
		return imports.Guild(self.discord,self.s,self.log).getGuildInvites(guildID)

	def getChannelInvites(self, channelID):
		return imports.Guild(self.discord,self.s,self.log).getChannelInvites(channelID)

	#get all guilds (this is used by the client when going to the developers portal)
	def getGuilds(self, with_counts=True):
		return imports.Guild(self.discord,self.s,self.log).getGuilds(with_counts)

	#get discoverable guilds
	def getDiscoverableGuilds(self, offset=0, limit=24):
		return imports.Guild(self.discord,self.s,self.log).getDiscoverableGuilds(offset, limit)

	def getGuildRegions(self, guildID):
		return imports.Guild(self.discord,self.s,self.log).getGuildRegions(guildID)

	#create a guild
	def createGuild(self, name, icon=None, channels=[], systemChannelID=None, template="2TffvPucqHkN"):
		return imports.Guild(self.discord,self.s,self.log).createGuild(name, icon, channels, systemChannelID, template)

	#delete a guild
	def deleteGuild(self, guildID):
		return imports.Guild(self.discord,self.s,self.log).deleteGuild(guildID)

	#kick a user
	def kick(self,guildID,userID,reason=""):
		return imports.Guild(self.discord,self.s,self.log).kick(guildID,userID,reason)

	#ban a user
	def ban(self,guildID,userID,deleteMessagesDays=0,reason=""):
		return imports.Guild(self.discord,self.s,self.log).ban(guildID,userID,deleteMessagesDays,reason)

	#unban a user
	def revokeBan(self, guildID, userID):
		return imports.Guild(self.discord,self.s,self.log).revokeBan(guildID, userID)

	#get number of members in each role
	def getRoleMemberCounts(self, guildID):
		return imports.Guild(self.discord,self.s,self.log).getRoleMemberCounts(guildID)

	#get integrations (includes applications aka bots)
	def getGuildIntegrations(self, guildID, include_applications=True):
		return imports.Guild(self.discord,self.s,self.log).getGuildIntegrations(guildID, include_applications)

	#get guild templates
	def getGuildTemplates(self, guildID):
		return imports.Guild(self.discord,self.s,self.log).getGuildTemplates(guildID)

	#get role member ids
	def getRoleMemberIDs(self, guildID, roleID):
		return imports.Guild(self.discord,self.s,self.log).getRoleMemberIDs(guildID, roleID)

	#add members to role (add a role to multiple members at the same time)
	def addMembersToRole(self, guildID, roleID, memberIDs):
		return imports.Guild(self.discord,self.s,self.log).addMembersToRole(guildID, roleID, memberIDs)

	#set roles of a member
	def setMemberRoles(self, guildID, memberID, roleIDs):
		return imports.Guild(self.discord,self.s,self.log).setMemberRoles(guildID, memberID, roleIDs)

	def getMemberVerificationData(self, guildID, with_guild=False, invite_code=None):
		return imports.Guild(self.discord,self.s,self.log).getMemberVerificationData(guildID, with_guild, invite_code)

	def agreeGuildRules(self, guildID, form_fields, version="2021-01-05T01:44:32.163000+00:00"):
		return imports.Guild(self.discord,self.s,self.log).agreeGuildRules(guildID, form_fields, version)

	def createThread(self, channelID, name, messageID=None, public=True, archiveAfter='24 hours'):
		return imports.Guild(self.discord,self.s,self.log).createThread(channelID, name, messageID, public, archiveAfter)

	def leaveThread(self, threadID, location="Sidebar Overflow"):
		return imports.Guild(self.discord,self.s,self.log).leaveThread(threadID, location)

	def joinThread(self, threadID, location="Banner"):
		return imports.Guild(self.discord,self.s,self.log).joinThread(threadID, location)

	def archiveThread(self, threadID, lock=True):
		return imports.Guild(self.discord,self.s,self.log).archiveThread(threadID, lock)

	def unarchiveThread(self, threadID, lock=False):
		return imports.Guild(self.discord,self.s,self.log).unarchiveThread(threadID, lock)

	def lookupSchool(self, email, allowMultipleGuilds=True):
		return imports.Guild(self.discord,self.s,self.log).lookupSchool(email, allowMultipleGuilds)

	def schoolHubSignup(self, email, school):
		return imports.Guild(self.discord,self.s,self.log).schoolHubSignup(email, school)

	'''
	Interactions
	'''
	#used when searching for slash commands in a dm w/a bot
	def getSlashCommands(self, applicationID):
		return imports.SlashCommands(self.discord,self.s,self.log).getSlashCommands(applicationID)

	#trigger a slash command (running /command blah blah blah whatever)
	def triggerSlashCommand(self, applicationID, channelID, guildID=None, data={}, nonce="calculate"):
		return imports.SlashCommands(self.discord,self.s,self.log).triggerSlashCommand(applicationID, channelID, guildID, data, nonce)

	#click on a button or select menu option(s)
	def click(self, applicationID, channelID, messageID, messageFlags, guildID=None, nonce="calculate", data={}):
		return imports.Buttons(self.discord,self.s,self.log).click(applicationID, channelID, messageID, messageFlags, guildID, nonce, data)

	'''
	"Science", aka Discord's tracking endpoint (https://luna.gitlab.io/discord-unofficial-docs/science.html - "Discord argues that they need to collect the data in the case the User allows the usage of the data later on. Which in [luna's] opinion is complete bullshit. Have a good day.")
	'''
	def initScience(self):
		try:
			#get analytics token
			response = imports.User(self.discord,self.s,self.log).info(with_analytics_token=True)
			if response.status_code == 401:
				raise
			self.userData = response.json() #this is essentially the connection test. We need it cause we can get important data without connecting to the gateway.
		except:
			self.userData = {"analytics_token": None, "id": "0"} #if token invalid
			#get xfingerprint
			if self.__xfingerprint == "":
				self.__xfingerprint = imports.Login(self.s, self.discord, self.log).getXFingerprint()
		#initialize Science object
		self.Science = imports.Science(self.discord, self.s, self.log, self.userData["analytics_token"], self.userData["id"], self.__xfingerprint)

	def science(self, events): #the real prep for science events happens down here, and only once for each client obj
		if self.Science == "":
			self.initScience()
		return self.Science.science(events)

	def calculateClientUUID(self, eventNum="default", userID="default", increment=True):
		if self.Science == "":
			self.initScience()
		return self.Science.UUIDobj.calculate(eventNum, userID, increment)

	def refreshClientUUID(self, resetEventNum=True):
		if self.Science == "":
			self.initScience()
		return self.Science.UUIDobj.refresh(resetEventNum)

	def parseClientUUID(self, client_uuid):
		if self.Science == "":
			self.Science = imports.Science(self.discord, self.s, self.log, None, "0", "") #no sequential data needed for parsing
			result = self.Science.UUIDobj.parse(client_uuid)
			self.Science = "" #reset
			return result
		else:
			return self.Science.UUIDobj.parse(client_uuid)

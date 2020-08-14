from .messages.messages import Messages
from .messages.embed import Embedder
from .user.user import User

from .Login import *
from .GatewayServer import *

import time
import random

class Settings:
	def __init__(self, obj):
		for k, v in obj.items():
			if isinstance(v, dict):
				setattr(self, k, Settings(v))
			else:
				setattr(self, k, v)
	def __getitem__(self, val):
		return self.__dict__[val]
	def __repr__(self):
		return '{%s}' % str(', '.join('%s : %s' % (k, repr(v)) for (k, v) in self.__dict__.items()))

class Client:
    def convert(self, data):
    	if isinstance(data, bytes):
    		return data.decode()
    	if isinstance(data, dict):
    		return dict(map(self.convert, data.items()))
    	if isinstance(data, tuple):
    		return tuple(map(self.convert, data))
    	if isinstance(data, list):
    		return list(map(self.convert, data))
    	return data
    def __init__(self, email="none", password="none", token="none", proxy_host=False, proxy_port=False): #not using None since that could get flagged by discord...
        self.__user_token = token
        self.__user_email = email
        self.__user_password = password
        self.__proxy_host = proxy_host
        self.__proxy_port = proxy_port
        self.classsession_settings = {} #look at function read()
        if self.__user_token == "none": #assuming email and pass are given...
        	self.__login = Login(self.__user_email, self.__user_password,self.__proxy_host,self.__proxy_port)
        	self.__user_token = self.__login.GetToken() #update token from "none" to true string value
        self.__gateway_server = GatewayServer(self.__proxy_host,self.__proxy_port)
        self.discord = 'https://discord.com/api/v8/'
        self.headers = {
        "Host": "discord.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.306 Chrome/78.0.3904.130 Electron/7.1.11 Safari/537.36",
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
        if self.__proxy_host != False and self.__proxy_port != False: #self.s.proxies defaults to {}
            self.proxies = {
            'http': self.__proxy_host+':'+self.__proxy_port,
            'https': self.__proxy_host+':'+self.__proxy_port
            }
            self.s.proxies.update(proxies)

    '''
    discord snowflake to unix timestamp and back

    '''
    def snowflake_to_unixts(self,snowflake):
        return int((snowflake/4194304+1420070400000)/1000)

    def unixts_to_snowflake(self,unixts):
        return int((unixts*1000-1420070400000)*4194304)

    '''
    (get) and/or read session settings/data
    '''
    def read(self,update=True): #returns a class, this is the main function, if you want ALL the session data (wall of data), then call this (or bot.read().__dict__). if update=False session_settings will not be updated
    	if update == False: #if read() hasnt been called yet this will just return an empty dict
    		return self.classsession_settings
    	self.__gateway_server.Connect(self.__user_token)
    	session_settings = self._Client__gateway_server._GatewayServer__session_settings
    	if isinstance(session_settings[b'_trace'],bytes): #if bytes shows up.......................idk sometimes it shows up sometimes it doesnt so this is just in case
    		session_settings[b'_trace'] = session_settings[b'_trace'][0].decode("utf-8")
    	strsession_settings = self.convert(session_settings) #this is a dict, the str denotes that there are no byte keys, only string keys
    	self.classsession_settings = Settings(strsession_settings)
    	return self.classsession_settings

    def getAnalyticsToken(self,update=True):
    	return self.read(update).analytics_token

    def getConnectedAccounts(self,update=True):
    	return self.read(update).connected_accounts

    def getConsents(self,update=True):
    	return self.read(update).consents

    def getExperiments(self,update=True):
    	return self.read(update).experiments

    def getFriendSuggestingCount(self,update=True): #no idea what this is but it's here so whatever
    	return self.read(update).friend_suggestion_count

    def getGuildExperiments(self,update=True):
    	return self.read(update).guild_experiments


    #All about guilds, oh geez this is a long one
    def getGuilds(self,update=True): #returns all information about all guilds you're in...might be a little overwhelming so don't call unless you're ready to see a wall of text
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	return [self.read(False).guilds[i] for i in range(len(self.read(False).guilds)) if i%2==0] #remove the erlang trash, which are on odd indices

    def getGuildIDs(self,update=True): #just get the guild ids, type list
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	return [self.getGuilds(False)[i]['id'] for i in range(len(self.getGuilds(False)))]


    ## getting specific about a PARTICULAR guild, note that guildID is an int, but if you happen to pass a string that's fine...I know most libs out there pass the guildID as a string so you might be used to doing that
    def getGuildData(self,guildID,update=True): #type dict, all data about a PARTICULAR guild, can be overwhelming, guildID is an int, but if you happen to pass a string that's fine
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	for i in range(len(self.getGuilds(False))):
    		if self.getGuilds(False)[i]['id'] == guildID:
    			return self.getGuilds(False)[i]
    	return None #guild not found

    def getGuildOwner(self,guildID,update=True):
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	return self.getGuildData(guildID,False)['owner_id'] #returns type int

    def getGuildBoostLvl(self,guildID,update=True):
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	return self.getGuildData(guildID,False)['premium_tier']

    def getGuildEmojis(self,guildID,update=True):
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	return self.getGuildData(guildID,False)['emojis']

    def getGuildBanner(self,guildID,update=True):
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	return self.getGuildData(guildID,False)['banner'] #if returns 'nil' then there's no banner

    def getGuildDiscoverySplash(self,guildID,update=True): #not sure what this is about, something about server discoverability i guess (https://discord.com/developers/docs/resources/guild)
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	return self.getGuildData(guildID,False)['discovery_splash']

    def getGuildUserPresences(self,guildID,update=True): #only returns presences of online, idle, or do-not-disturb users
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	return [self.getGuildData(guildID,False)['presences'][i] for i in range(len(self.getGuildData(guildID,False)['presences'])) if i%2==0]

    def getGuildMsgNotificationSettings(self,guildID,update=True): #returns an int, 0=all messages, 1=only mentions (https://discord.com/developers/docs/resources/guild#guild-object-default-message-notification-level)
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	return self.getGuildData(guildID,False)['default_message_notifications']

    def getGuildRulesChannelID(self,guildID,update=True): #nil if no rules channel id, idk if this always works so it might actually be more useful just to look for the word "rules" in channel names
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	return self.getGuildData(guildID,False)['rules_channel_id']

    def getGuildVerificationLvl(self,guildID,update=True): #returns an int, 0-4 (https://discord.com/developers/docs/resources/guild#guild-object-verification-level)
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	return self.getGuildData(guildID,False)['verification_level']

    def getGuildFeatures(self,guildID,update=True): #returns a list of strings (https://discord.com/developers/docs/resources/guild#guild-object-guild-features)
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	return self.getGuildData(guildID,False)['features']

    def getGuildJoinTime(self,guildID,update=True): #returns when you joined the server, type string
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	return self.getGuildData(guildID,False)['joined_at']

    def getGuildRegion(self,guildID,update=True):
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	return self.getGuildData(guildID,False)['region']

    def getGuildApplicationID(self,GuildID,update=True): #returns application id of the guild creator if it is bot-created (https://discord.com/developers/docs/resources/guild#guild-object-guild-features)
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	return self.getGuildData(guildID,False)['application_id']

    def getGuildAfkChannelID(self,guildID,update=True): #not sure what this is
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	return self.getGuildData(guildID,False)['afk_channel_id']

    def getGuildIcon(self,guildID,update=True): #https://discord.com/developers/docs/reference#image-formatting
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	return self.getGuildData(guildID,False)['icon']

    def getGuildName(self,guildID,update=True):
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	return self.getGuildData(guildID,False)['name']

    def getGuildMaxVideoChannelUsers(self,guildID,update=True):
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	return self.getGuildData(guildID,False)['max_video_channel_users']

    def getGuildRoles(self,guildID,update=True): #https://discord.com/developers/docs/topics/permissions#role-object
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	return [self.getGuildData(guildID,False)['roles'][i] for i in range(len(self.getGuildData(guildID,False)['roles'])) if i%2==0]

    def getGuildPublicUpdatesChannelID(self,guildID,update=True):
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	return self.getGuildData(guildID,False)['public_updates_channel_id']

    def getGuildSystemChannelFlags(self,guildID,update=True): #https://discord.com/developers/docs/resources/guild#guild-object-system-channel-flags
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	return self.getGuildData(guildID,False)['system_channel_flags']

    def getGuildMfaLvl(self,guildID,update=True): #https://discord.com/developers/docs/resources/guild#guild-object-mfa-level
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	return self.getGuildData(guildID,False)['mfa_level']

    def getGuildAfkTimeout(self,guildID,update=True): #returns type int, unit seconds, https://discord.com/developers/docs/resources/guild
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	return self.getGuildData(guildID,False)['afk_timeout']

    def getGuildHashes(self,guildID,update=True): #https://github.com/discord/discord-api-docs/issues/1642
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	return self.getGuildData(guildID,False)['guild_hashes']

    def getGuildSystemChannelID(self,guildID,update=True): #returns an int, the id of the channel where guild notices such as welcome messages and boost events are posted
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	return self.getGuildData(guildID,False)['system_channel_id']

    def isGuildLazy(self,guildID,update=True): #slightly different naming format since it returns a boolean (https://luna.gitlab.io/discord-unofficial-docs/lazy_guilds.html)
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	if self.getGuildData(guildID,False)['lazy'] == 'true':
    		return True
    	else:
    		return False

    def getGuildNumBoosts(self,guildID,update=True): #get number of boosts the server has gotten
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	return self.getGuildData(guildID,False)['premium_subscription_count']

    def isGuildLarge(self,guildID,update=True): #slightly different naming format since it returns a boolean, large if more than 250 members
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	if self.getGuildData(guildID,False)['large'] == 'true':
    		return True
    	else:
    		return False

    def getGuildExplicitContentFilter(self,guildID,update=True): #https://discord.com/developers/docs/resources/guild#guild-object-explicit-content-filter-level
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	return self.getGuildData(guildID,False)['explicit_content_filter']

    def getGuildSplashHash(self,guildID,update=True): #not sure what this is for
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	return self.getGuildData(guildID,False)['splash']

    def getGuildVoiceStates(self,guildID,update=True): #https://discord.com/developers/docs/resources/voice#voice-state-object
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	return [self.getGuildData(guildID,False)['voice_states'][i] for i in range(len(self.getGuildData(guildID,False)['voice_states'])) if i%2==0]

    def getGuildMemberCount(self,guildID,update=True):
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	return self.getGuildData(guildID,False)['member_count']

    def getGuildDescription(self,guildID,update=True):
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	return self.getGuildData(guildID,False)['description']

    def getGuildVanityUrlCode(self,guildID,update=True):
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	return self.getGuildData(guildID,False)['vanity_url_code']

    def getGuildPreferredLocale(self,guildID,update=True):
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	return self.getGuildData(guildID,False)['preferred_locale']

    def getGuildAllChannels(self,guildID,update=True): #returns all categories and all channels, all the data about that, wall of data so it can be a bit overwhelming, useful if you want to check how many channels your server has since discord counts categories as channels
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	return [self.getGuildData(guildID,False)['channels'][i] for i in range(len(self.getGuildData(guildID,False)['channels'])) if i%2==0]

    def getGuildCategories(self,guildID,update=True): #all data about all guild categories, can be overwhelming
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	all_channels = [self.getGuildData(guildID,False)['channels'][i] for i in range(len(self.getGuildData(guildID,False)['channels'])) if i%2==0]
    	all_categories = []
    	for channel in all_channels: #https://discord.com/developers/docs/resources/channel#channel-object-channel-types
    		if channel['type'] == 4:
    			all_categories.append(channel)
    	return all_categories

    def getGuildCategoryIDs(self,guildID,update=True):
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	return [self.getGuildCategories(guildID,False)[i]['id'] for i in range(len(self.getGuildCategories(guildID,False)))]

    def getGuildCategoryData(self,guildID,categoryID,update=True):
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	if isinstance(categoryID,str):
    		categoryID = int(categoryID)
    	for i in range(len(self.getGuildCategories(guildID,False))):
    		if self.getGuildCategories(guildID,False)[i]['id'] == categoryID:
    			return self.getGuildCategories(guildID,False)[i]
    	return None #category not found

    def getGuildChannels(self,guildID,update=True): #all data about all guild channels, can be overwhelming
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	all_channels = [self.getGuildData(guildID,False)['channels'][i] for i in range(len(self.getGuildData(guildID,False)['channels'])) if i%2==0]
    	all_non_categories = []
    	for channel in all_channels: #https://discord.com/developers/docs/resources/channel#channel-object-channel-types
    		if channel['type'] != 4:
    			all_non_categories.append(channel)
    	return all_non_categories

    def getGuildChannelIDs(self,guildID,update=True):
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	return [self.getGuildChannels(guildID,False)[i]['id'] for i in range(len(self.getGuildChannels(guildID,False)))]

    def getGuildChannelData(self,guildID,channelID,update=True):
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	if isinstance(channelID,str):
    		channelID = int(channelID)
    	for i in range(len(self.getGuildChannels(guildID,False))):
    		if self.getGuildChannels(guildID,False)[i]['id'] == channelID:
    			return self.getGuildChannels(guildID,False)[i]
    	return None #channel not found

    def getGuildMembers(self,guildID,update=True): #all data about all members, can be overwhelming....doesnt get all members for some reason...my guess is that it only gets most recently active members but idk
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	return [self.getGuildData(guildID,False)['members'][i] for i in range(len(self.getGuildData(guildID,False)['members'])) if i%2==0]

    def getGuildMemberIDs(self,guildID,update=True):
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	return [self.getGuildMembers(guildID,False)[i]['user']['id'] for i in range(len(self.getGuildMembers(guildID,False)))]

    def getGuildMemberData(self,guildID,memberID,update=True):
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(guildID,str):
    		guildID = int(guildID)
    	if isinstance(memberID,str):
    		memberID = int(memberID)
    	for i in range(len(self.getGuildMembers(guildID,False))):
    		if self.getGuildMembers(guildID,False)[i]['user']['id'] == memberID:
    			return self.getGuildMembers(guildID,False)[i]
    	return None #member not found, again I must state that getGuildMembers doesnt return all members, likely it only returns most recent members but who knows for now...

    # end of guild stuff, now onto the other stuff

    def getNotes(self,update=True):
    	return self.read(update).notes #returns a dict where the keys are user IDs and the values are the notes

    def getOnlineFriends(self,update=True): #i saw no reason to make "sub functions" of this since it's only about online friends
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	[self.read(False).presences[i] for i in range(len(self.read(False).presences)) if i%2==0]

    #all about DMs, aw geez this is gonna be a long one too i guess...
    def getDMs(self,update=True):
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	return [self.read(False).private_channels[i] for i in range(len(self.read(False).private_channels)) if i%2==0]

    def getDMIDs(self,update=True): #discord sometimes calls these channel IDs...
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	return [self.getDMs(False)[i]['id'] for i in range(len(self.getDMs(False)))]

    def getDMData(self,DMID,update=True): #get data about a particular DM
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(DMID,str):
    		DMID = int(DMID)
    	for i in range(len(self.getDMs(False))):
    		if self.getDMs(False)[i]['id'] == DMID:
    			return self.getDMs(False)[i]
    	return None

    def getDMRecipients(self,DMID,update=True): #returns everyone in that DM except your user
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	if isinstance(DMID,str):
    		DMID = int(DMID)
    	return [self.getDMData(DMID,False)['recipients'][i] for i in range(len(self.getDMData(DMID,False)['recipients'])) if i%2==0]

    #end of DM stuff, heh that wasnt that bad, onto the rest of the stuff

    def getReadStates(self,update=True): #another advantage of using websockets instead of requests (see https://github.com/discord/discord-api-docs/issues/13)
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	return [self.read(False).read_state[i] for i in range(len(self.read(False).read_state)) if i%2==0]

    #all about relationships...on discord. note this includes all your friends AND all users youve blocked
    def getRelationships(self,update=True):
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	return [self.read(False).relationships[i] for i in range(len(self.read(False).relationships)) if i%2==0]

    def getRelationshipIDs(self,update=True): #gets userIDs that are in a "relationship" with your account
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	return [self.getRelationships(False)[i]['id'] for i in range(len(self.getRelationships(False)))]

    def getRelationshipData(self,RelationshipID,update=True):
        getthatdata = self.read(update) #refreshes session settings if update is True
        if isinstance(RelationshipID,str) and "#" in RelationshipID: #if in username discriminator format
            for i in range(len(self.getRelationships(False))):
                if self.getRelationships(False)[i]['user']['username'] == RelationshipID.split("#")[0] and self.getRelationships(False)[i]['user']['discriminator'] == RelationshipID.split("#")[1]:
                    return self.getRelationships(False)[i]
        elif isinstance(RelationshipID,str): #if in ID format, but is a string instead of an int
            RelationshipID = int(RelationshipID)
        for i in range(len(self.getRelationships(False))):
            if self.getRelationships(False)[i]['id'] == RelationshipID:
                return self.getRelationships(False)[i]
        return None

    def getFriends(self,update=True): #yay, no this will not give you friends, it returns data about the users you have a friends
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	friends = []
    	for i in range(len(self.getRelationships(False))):
    		if self.getRelationships(False)[i]['type'] == 1:
    			friends.append(self.getRelationships(False)[i])
    	return friends #wow and just like that you have friends.........................

    def getFriendIDs(self,update=True):
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	return [self.getFriends(False)[i]['id'] for i in range(len(self.getFriends(False)))]

    def getBlocked(self,update=True): #nay
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	blocked = []
    	for i in range(len(self.getRelationships(False))):
    		if self.getRelationships(False)[i]['type'] == 2:
    			blocked.append(self.getRelationships(False)[i])
    	return blocked

    def getBlockedIDs(self,update=True):
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	return [self.getBlocked(False)[i]['id'] for i in range(len(self.getBlocked(False)))]

    def getIncomingFriendRequests(self,update=True): #returns data...
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	ifr = []
    	for i in range(len(self.getRelationships(False))):
    		if self.getRelationships(False)[i]['type'] == 3:
    			ifr.append(self.getRelationships(False)[i])
    	return ifr

    def getIncomingFriendRequestIDs(self,update=True):
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	return [self.getIncomingFriendRequests(False)[i]['id'] for i in range(len(self.getIncomingFriendRequests(False)))]

    def getOutgoingFriendRequests(self,update=True):
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	ofr = []
    	for i in range(len(self.getRelationships(False))):
    		if self.getRelationships(False)[i]['type'] == 4:
    			ofr.append(self.getRelationships(False)[i])
    	return ofr

    def getOutgoingFriendRequestIDs(self,update=True):
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	return [self.getOutgoingFriendRequests(False)[i]['id'] for i in range(len(self.getOutgoingFriendRequests(False)))]

    #end of relationship stuff

    def getSessionID(self,update=True):
    	return self.read(update).session_id

    def getTutorial(self,update=True): #tutorial on what? guess we'll never know...ask discord maybe?
    	return self.read(update).tutorial

    def getUserData(self,update=True):
    	return self.read(update).user

    def getUserGuildSettings(self,update=True,guildID=None): #personal settings for a server, like whether or not you want @everyone pings to show, formatting is weird cause you might not want to pass a guildID, hence it is at the end
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	all_user_guild_settings = [self.read(False).user_guild_settings[i] for i in range(len(self.read(False).user_guild_settings)) if i%2==0]
    	if guildID != None:
    		if isinstance(guildID,str):
    			guildID = int(guildID)
    		for i in range(len(all_user_guild_settings)):
    			if all_user_guild_settings[i]['guild_id'] == guildID:
    				return all_user_guild_settings[i]
    	else:
    		return all_user_guild_settings

    def getUserSettings(self,update=True): #returns a class
    	return self.read(update).user_settings

    def getOptionsForUserSettings(self,update=True): #bc i didnt feel like making a ton of sub functions for this, the data is there if you want to process it but rn it seems useless to me
    	return list(self.read(update).user_settings.__dict__.keys()) #since getUserSettings() returns a class, you can call subsettings using this format: getUserSettings().afk_timeout

    def getWebsocketVersion(self,update=True):
    	return self.read(update).v

    # oof end of reading session settings


    '''
    username to snowflake and back
    '''
    def username_to_userID(self,userdiscriminator): #userdiscriminator is "username#discriminator"
        getthatdata = self.read() #might as well get current session settings
        if type(self.getRelationshipData(userdiscriminator,False)).__name__ != 'NoneType': #testing our luck to see if user is in a "relationship" with our user
            return self.getRelationshipData(userdiscriminator,False)['id'] #returns type int
        User(self.discord,self.s).requestFriend(userdiscriminator) #this puts you in a "relationship" with that user
        if type(self.getRelationshipData(userdiscriminator,True)).__name__ != 'NoneType': #if you sent a request to a bot or to yourself then this becomes False
            User(self.discord,self.s).removeRelationship(self.getRelationshipData(userdiscriminator,False)['id'])
            return self.getRelationshipData(userdiscriminator,False)['id'] #returns type int
        return None #happens if other user is a bot, is yourself, does not exist, or something wrong with your account

    def userID_to_username(self,userID): #userID aka snowflake
        getthatdata = self.read() #might as well get current session settings
        if type(self.getRelationshipData(snowflake,False)).__name__ != 'NoneType': #testing our luck to see if user is in a "relationship" with our user
            userdiscriminator = self.getRelationshipData(snowflake,False)['user']['username'] + "#" + self.getRelationshipData(snowflake,False)['user']['discriminator']
            return userdiscriminator
        if isinstance(snowflake,int):
            snowflake = str(snowflake)
        User(self.discord,self.s).requestFriend(snowflake) #this puts you in a "relationship" with that user
        if type(self.getRelationshipData(snowflake,True)).__name__ != 'NoneType': #if you sent a request to a bot or to yourself then this becomes False
            User(self.discord,self.s).removeRelationship(snowflake)
            userdiscriminator = self.getRelationshipData(snowflake,False)['user']['username'] + "#" + self.getRelationshipData(snowflake,False)['user']['discriminator']
            return userdiscriminator
        return None #happens if other user is a bot, is yourself, does not exist, or something wrong with your account


    '''
    Messages
    '''
    #get recent messages
    def getMessages(self,channelID,num=1,beforeDate=None): # num <= 100, beforeDate is a snowflake
        if isinstance(channelID,int):
            channelID = str(channelID)
        return Messages(self.discord,self.s).getRecentMessage(channelID,num,beforeDate)

    #send text or embed messages
    def sendMessage(self,channelID,message,embed="",tts=False):
        if isinstance(channelID,int):
            channelID = str(channelID)
        return Messages(self.discord,self.s).sendMessage(channelID,message,embed,tts)

    #send files (local or link)
    def sendFile(self,channelID,filelocation,isurl=False,message=""):
        if isinstance(channelID,int):
            channelID = str(channelID)
        return Messages(self.discord,self.s).sendFile(channelID,filelocation,isurl,message)

    #search messages
    def searchMessages(self,guildID,channelID=None,userID=None,mentionsUserID=None,has=None,beforeDate=None,afterDate=None,textSearch=None,afterNumResults=None):
        if isinstance(guildID,int):
            guildID = str(guildID)
        return Messages(self.discord,self.s).searchMessages(guildID,channelID,userID,mentionsUserID,has,beforeDate,afterDate,textSearch,afterNumResults)

    #filter searchMessages, takes in the output of searchMessages (a requests response object) and outputs a list of target messages
    def filterSearchResults(self,searchResponse):
        return Messages(self.discord,self.s).filterSearchResults(searchResponse)

    #sends the typing action for 10 seconds (or technically until you change the page)
    def typingAction(self,channelID):
        if isinstance(channelID,int):
            channelID = str(channelID)
        return Messages(self.discord,self.s).typingAction(channelID)

    #delete message
    def deleteMessage(self,channelID,messageID):
        if isinstance(channelID,int):
            channelID = str(channelID)
        if isinstance(messageID,int):
            messageID = str(messageID)
        return Messages(self.discord,self.s).deleteMessage(channelID,messageID)

    #pin message
    def pinMessage(self,channelID,messageID):
        if isinstance(channelID,int):
            channelID = str(channelID)
        if isinstance(messageID,int):
            messageID = str(messageID)
        return Messages(self.discord,self.s).pinMessage(channelID,messageID)

    #un-pin message
    def unPinMessage(self,channelID,messageID):
        if isinstance(channelID,int):
            channelID = str(channelID)
        if isinstance(messageID,int):
            messageID = str(messageID)
        return Messages(self.discord,self.s).unPinMessage(channelID,messageID)

    #get pinned messages
    def getPins(self,channelID):
        if isinstance(channelID,int):
            channelID = str(channelID)
        return Messages(self.discord,self.s).getPins(channelID)

    '''
    User relationships
    '''
    #create outgoing friend request
    def requestFriend(self,user): #you can input a userID(snowflake) or a user discriminator
        if isinstance(user,int): #only affects userIDs cause...well...strings...
            user = str(user)
        return User(self.discord,self.s).requestFriend(user)

    #accept incoming friend request
    def acceptFriend(self,userID):
        if isinstance(userID,int):
            userID = str(userID)
        return User(self.discord,self.s).acceptFriend(userID)

    #remove friend OR unblock user
    def removeRelationship(self,userID):
        if isinstance(userID,int):
            userID = str(userID)
        return User(self.discord,self.s).removeRelationship(userID)

    #block user
    def blockUser(self,userID):
        if isinstance(userID,int):
            userID = str(userID)
        return User(self.discord,self.s).blockUser(userID)

    '''
    Profile edits
    '''
    # change name
    def changeName(self,name):
        return User(self.discord,self.s).changeName(self.email,self.password,name)
    # set status
    def setStatus(self,status):
        return User(self.discord,self.s).setStatus(status)
    # set avatar
    def setAvatar(self,imagePath):
        return User(self.discord,self.s).setAvatar(self.email,self.password,imagePath)

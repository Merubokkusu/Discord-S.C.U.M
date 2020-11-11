from .guild.guild import Guild
from .messages.messages import Messages
from .messages.embed import Embedder
from .user.user import User

from .login.Login import *
from .gateway.GatewayServer import *

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
        self.__proxy_host = proxy_host
        self.__proxy_port = proxy_port
        self.session_settings = [] #consists of 2 parts, READY and READY_SUPPLEMENTAL; look at function read()
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
        if self.__proxy_host not in (None,False): #self.s.proxies defaults to {}
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
        self.__gateway_server = GatewayServer(self.websocketurl,self.__user_token,self.ua_data,self.__proxy_host,self.__proxy_port,self.log)

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
    (get) and/or read session settings/data (this section is all about reading the READY and READY_SUPPLEMENTAL responses after connecting to discord's gateway server)
    '''
    def read(self,update=True):
        if update == False:
            if self.session_settings == []:
                raise SessionSettingsError('Session Settings not collected yet. Your first gateway interaction needs update to be set to True. For example: bot.read(True)')
            return self.session_settings
        self.__gateway_server.run('get session data',log=self.log)
        self.session_settings = [self._Client__gateway_server.session_data_1['d'], self._Client__gateway_server.session_data_2['d']]
        return self.session_settings

    #Parsing guild data from 1st part of session data (from READY)
    def getGuilds(self,update=True): #returns all information about all guilds you're in...might be a little overwhelming so don't call unless you're ready to see a wall of text
        return self.read(update)[0]['guilds']

    def getGuildIDs(self,update=True): #just get the guild ids, type list
        getthatdata = self.read(update) #refreshes session settings if update is True
        return [self.getGuilds(False)[i]['id'] for i in range(len(self.getGuilds(False)))]

    ## getting specific about a PARTICULAR guild
    def getGuildData(self,guildID,update=True): #type dict, all data about a PARTICULAR guild, can be overwhelming
        getthatdata = self.read(update) #refreshes session settings if update is True
        for i in range(len(self.getGuilds(False))):
            if self.getGuilds(False)[i]['id'] == guildID:
                return self.getGuilds(False)[i]
        return None #guild not found

    def getGuildOwner(self,guildID,update=True):
        getthatdata = self.read(update) #refreshes session settings if update is True
        return self.getGuildData(guildID,False)['owner_id'] #returns type int

    def getGuildBoostLvl(self,guildID,update=True):
        getthatdata = self.read(update) #refreshes session settings if update is True
        return self.getGuildData(guildID,False)['premium_tier']

    def getGuildEmojis(self,guildID,update=True):
        getthatdata = self.read(update) #refreshes session settings if update is True
        return self.getGuildData(guildID,False)['emojis']

    def getGuildBanner(self,guildID,update=True):
        getthatdata = self.read(update) #refreshes session settings if update is True
        return self.getGuildData(guildID,False)['banner'] #if returns 'nil' then there's no banner

    def getGuildDiscoverySplash(self,guildID,update=True): #not sure what this is about, something about server discoverability i guess (https://discord.com/developers/docs/resources/guild)
        getthatdata = self.read(update) #refreshes session settings if update is True
        return self.getGuildData(guildID,False)['discovery_splash']

    def getGuildMsgNotificationSettings(self,guildID,update=True): #returns an int, 0=all messages, 1=only mentions (https://discord.com/developers/docs/resources/guild#guild-object-default-message-notification-level)
        getthatdata = self.read(update) #refreshes session settings if update is True
        return self.getGuildData(guildID,False)['default_message_notifications']

    def getGuildRulesChannelID(self,guildID,update=True): #nil if no rules channel id, idk if this always works so it might actually be more useful just to look for the word "rules" in channel names
        getthatdata = self.read(update) #refreshes session settings if update is True
        return self.getGuildData(guildID,False)['rules_channel_id']

    def getGuildVerificationLvl(self,guildID,update=True): #returns an int, 0-4 (https://discord.com/developers/docs/resources/guild#guild-object-verification-level)
        getthatdata = self.read(update) #refreshes session settings if update is True
        return self.getGuildData(guildID,False)['verification_level']

    def getGuildFeatures(self,guildID,update=True): #returns a list of strings (https://discord.com/developers/docs/resources/guild#guild-object-guild-features)
        getthatdata = self.read(update) #refreshes session settings if update is True
        return self.getGuildData(guildID,False)['features']

    def getGuildJoinTime(self,guildID,update=True): #returns when you joined the server, type string
        getthatdata = self.read(update) #refreshes session settings if update is True
        return self.getGuildData(guildID,False)['joined_at']

    def getGuildRegion(self,guildID,update=True):
        getthatdata = self.read(update) #refreshes session settings if update is True
        return self.getGuildData(guildID,False)['region']

    def getGuildApplicationID(self,guildID,update=True): #returns application id of the guild creator if it is bot-created (https://discord.com/developers/docs/resources/guild#guild-object-guild-features)
        getthatdata = self.read(update) #refreshes session settings if update is True
        return self.getGuildData(guildID,False)['application_id']

    def getGuildAfkChannelID(self,guildID,update=True): #not sure what this is
        getthatdata = self.read(update) #refreshes session settings if update is True
        return self.getGuildData(guildID,False)['afk_channel_id']

    def getGuildIcon(self,guildID,update=True): #https://discord.com/developers/docs/reference#image-formatting
        getthatdata = self.read(update) #refreshes session settings if update is True
        return self.getGuildData(guildID,False)['icon']

    def getGuildName(self,guildID,update=True):
        getthatdata = self.read(update) #refreshes session settings if update is True
        return self.getGuildData(guildID,False)['name']

    def getGuildMaxVideoChannelUsers(self,guildID,update=True):
        getthatdata = self.read(update) #refreshes session settings if update is True
        return self.getGuildData(guildID,False)['max_video_channel_users']

    def getGuildRoles(self,guildID,update=True): #https://discord.com/developers/docs/topics/permissions#role-object
        getthatdata = self.read(update) #refreshes session settings if update is True
        return self.getGuildData(guildID,False)['roles']

    def getGuildPublicUpdatesChannelID(self,guildID,update=True):
        getthatdata = self.read(update) #refreshes session settings if update is True
        return self.getGuildData(guildID,False)['public_updates_channel_id']

    def getGuildSystemChannelFlags(self,guildID,update=True): #https://discord.com/developers/docs/resources/guild#guild-object-system-channel-flags
        getthatdata = self.read(update) #refreshes session settings if update is True
        return self.getGuildData(guildID,False)['system_channel_flags']

    def getGuildMfaLvl(self,guildID,update=True): #https://discord.com/developers/docs/resources/guild#guild-object-mfa-level
        getthatdata = self.read(update) #refreshes session settings if update is True
        return self.getGuildData(guildID,False)['mfa_level']

    def getGuildAfkTimeout(self,guildID,update=True): #returns type int, unit seconds, https://discord.com/developers/docs/resources/guild
        getthatdata = self.read(update) #refreshes session settings if update is True
        return self.getGuildData(guildID,False)['afk_timeout']

    def getGuildHashes(self,guildID,update=True): #https://github.com/discord/discord-api-docs/issues/1642
        getthatdata = self.read(update) #refreshes session settings if update is True
        return self.getGuildData(guildID,False)['guild_hashes']

    def getGuildSystemChannelID(self,guildID,update=True): #returns an int, the id of the channel where guild notices such as welcome messages and boost events are posted
        getthatdata = self.read(update) #refreshes session settings if update is True
        return self.getGuildData(guildID,False)['system_channel_id']

    def isGuildLazy(self,guildID,update=True): #slightly different naming format since it returns a boolean (https://luna.gitlab.io/discord-unofficial-docs/lazy_guilds.html)
        getthatdata = self.read(update) #refreshes session settings if update is True
        if self.getGuildData(guildID,False)['lazy'] == 'true':
            return True
        else:
            return False

    def getGuildNumBoosts(self,guildID,update=True): #get number of boosts the server has gotten
        getthatdata = self.read(update) #refreshes session settings if update is True
        return self.getGuildData(guildID,False)['premium_subscription_count']

    def isGuildLarge(self,guildID,update=True): #slightly different naming format since it returns a boolean, large if more than 250 members
        getthatdata = self.read(update) #refreshes session settings if update is True
        if self.getGuildData(guildID,False)['large'] == 'true':
            return True
        else:
            return False

    def getGuildExplicitContentFilter(self,guildID,update=True): #https://discord.com/developers/docs/resources/guild#guild-object-explicit-content-filter-level
        getthatdata = self.read(update) #refreshes session settings if update is True
        return self.getGuildData(guildID,False)['explicit_content_filter']

    def getGuildSplashHash(self,guildID,update=True): #not sure what this is for
        getthatdata = self.read(update) #refreshes session settings if update is True
        return self.getGuildData(guildID,False)['splash']

    def getGuildMemberCount(self,guildID,update=True):
        getthatdata = self.read(update) #refreshes session settings if update is True
        return self.getGuildData(guildID,False)['member_count']

    def getGuildDescription(self,guildID,update=True):
        getthatdata = self.read(update) #refreshes session settings if update is True
        return self.getGuildData(guildID,False)['description']

    def getGuildVanityUrlCode(self,guildID,update=True):
        getthatdata = self.read(update) #refreshes session settings if update is True
        return self.getGuildData(guildID,False)['vanity_url_code']

    def getGuildPreferredLocale(self,guildID,update=True):
        getthatdata = self.read(update) #refreshes session settings if update is True
        return self.getGuildData(guildID,False)['preferred_locale']

    def getGuildAllChannels(self,guildID,update=True): #returns all categories and all channels, all the data about that, wall of data so it can be a bit overwhelming, useful if you want to check how many channels your server has since discord counts categories as channels
        getthatdata = self.read(update) #refreshes session settings if update is True
        return self.getGuildData(guildID,False)['channels']

    def getGuildCategories(self,guildID,update=True): #all data about all guild categories, can be overwhelming
        getthatdata = self.read(update) #refreshes session settings if update is True
        all_channels = self.getGuildData(guildID,False)['channels']
        all_categories = []
        for channel in all_channels: #https://discord.com/developers/docs/resources/channel#channel-object-channel-types
            if channel['type'] == 4:
                all_categories.append(channel)
        return all_categories

    def getGuildCategoryIDs(self,guildID,update=True):
        getthatdata = self.read(update) #refreshes session settings if update is True
        return [self.getGuildCategories(guildID,False)[i]['id'] for i in range(len(self.getGuildCategories(guildID,False)))]

    def getGuildCategoryData(self,guildID,categoryID,update=True):
        getthatdata = self.read(update) #refreshes session settings if update is True
        for i in range(len(self.getGuildCategories(guildID,False))):
            if self.getGuildCategories(guildID,False)[i]['id'] == categoryID:
                return self.getGuildCategories(guildID,False)[i]
        return None #category not found

    def getGuildChannels(self,guildID,update=True): #all data about all guild channels, can be overwhelming
        getthatdata = self.read(update) #refreshes session settings if update is True
        all_channels = self.getGuildData(guildID,False)['channels']
        all_non_categories = []
        for channel in all_channels: #https://discord.com/developers/docs/resources/channel#channel-object-channel-types
            if channel['type'] != 4:
                all_non_categories.append(channel)
        return all_non_categories

    def getGuildChannelIDs(self,guildID,update=True):
        getthatdata = self.read(update) #refreshes session settings if update is True
        return [self.getGuildChannels(guildID,False)[i]['id'] for i in range(len(self.getGuildChannels(guildID,False)))]

    def getGuildChannelData(self,guildID,channelID,update=True):
        getthatdata = self.read(update) #refreshes session settings if update is True
        for i in range(len(self.getGuildChannels(guildID,False))):
            if self.getGuildChannels(guildID,False)[i]['id'] == channelID:
                return self.getGuildChannels(guildID,False)[i]
        return None #channel not found

    #Parsing guild data from 2nd part of session data (from READY_SUPPLEMENTAL)
    def getGuildVoiceStates(self,guildID,update=True): #https://discord.com/developers/docs/resources/voice#voice-state-object
        getthatdata = self.read(update) #refreshes session settings if update is True
        guildIndex = self.getGuildIDs(False).index(guildID)
        return self.read(False)[1]['guilds'][guildIndex]['voice_states']

    def getGuildNotOfflineCachedMembers(self,guildID,update=True): #so, not offline, but not all the not-offline members so....not offline cached members. I know I know long function name, but it's descriptive.
        getthatdata = self.read(update) #refreshes session settings if update is True
        guildIndex = self.getGuildIDs(False).index(guildID)
        return self.read(False)[1]['merged_members'][guildIndex]

    def getGuildNotOfflineCachedMemberIDs(self,guildID,update=True):
        getthatdata = self.read(update) #refreshes session settings if update is True
        return [self.getGuildCachedMembers(guildID,False)[i]['user_id'] for i in range(len(self.getGuildCachedMembers(guildID,False)))]

    def getGuildNotOfflineCachedMemberData(self,guildID,userID,update=True):
        getthatdata = self.read(update) #refreshes session settings if update is True
        for i in range(len(self.getGuildNotOfflineCachedMembers(guildID,False))):
            if self.getGuildNotOfflineCachedMembers(guildID,False)[i]['user_id'] == userID:
                return self.getGuildNotOfflineCachedMembers(guildID,False)[i]
        return None

    def getMergedPresences(self,update=True): #includes both guild and friend presences, but only the users that are not offline
        return self.read(update)[1]['merged_presences']

    def getAllGuildsMergedPresences(self,update=True):
        return self.read(update)[1]['merged_presences']['guilds']

    def getGuildMergedPresences(self,guildID,update=True): #this is different from getGuildNotOfflineCachedMembers because you can see presence data. also, not sure why, but a diff number of members shows up here than getGuildNotOfflineCachedMembers
        getthatdata = self.read(update) #refreshes session settings if update is True
        guildIndex = self.getGuildIDs(False).index(guildID)
        return self.read(False)[1]['merged_presences']['guilds'][guildIndex]

    def getGuildMergedPresencesIDs(self,update=True):
        getthatdata = self.read(update) #refreshes session settings if update is True
        return [self.getGuildMergedPresences(guildID,False)[i]['user_id'] for i in range(len(self.getGuildMergedPresences(guildID,False)))]

    def getGuildMergedPresencesData(self,guildID,userID,update=True):
        getthatdata = self.read(update) #refreshes session settings if update is True
        for i in range(len(self.getGuildMergedPresences(guildID,False))):
            if self.getGuildMergedPresences(guildID,False)[i]['user_id'] == userID:
                return self.getGuildMergedPresences(guildID,False)[i]
        return None

    def getAllFriendsMergedPresences(self,update=True):
        return self.read(update)[1]['merged_presences']['friends']

    def getAllFriendsMergedPresencesIDs(self,update=True): #get the user IDs from getAllFriendsMergedPresences
        getthatdata = self.read(update) #refreshes session settings if update is True
        return [self.getAllFriendsMergedPresences(False)[i]['user_id'] for i in range(len(self.getAllFriendsMergedPresences(False)))]

    def getFriendMergedPresencesData(self,userID,update=True):
        getthatdata = self.read(update) #refreshes session settings if update is True
        for i in range(len(self.getAllFriendsMergedPresences(False))):
            if self.getAllFriendsMergedPresences(False)[i]['user_id'] == userID:
                return self.getAllFriendsMergedPresences(False)[i]
        return None

    def getAllMyGuildPositions(self,update=True): #if you have a better name for this, pls let me know. It outputs your roles, nick, joined at, etc for each guild.
        return self.read(update)[0]['merged_members']

    def getMyGuildPosition(self,guildID,update=True):
        getthatdata = self.read(update) #refreshes session settings if update is True
        guildIndex = self.getGuildIDs(False).index(guildID)
        return self.read(False)[0]['merged_members'][guildIndex][0]

    #################

    def getAnalyticsToken(self,update=True):
        return self.read(update)[0]['analytics_token']

    def getConnectedAccounts(self,update=True):
        return self.read(update)[0]['connected_accounts']

    def getConsents(self,update=True):
        return self.read(update)[0]['consents']

    def getExperiments(self,update=True):
        return self.read(update)[0]['experiments']

    def getFriendSuggestionCount(self,update=True): #no idea what this is but it's here so whatever
        return self.read(update)[0]['friend_suggestion_count']

    def getGuildExperiments(self,update=True):
        return self.read(update)[0]['guild_experiments']

    def getNotOfflineFriends(self,update=True): #because there's a distinction between online and dnd and idle
        return self.read(update)[1]['merged_presences']['friends']

    #all about DMs
    def getDMs(self,update=True):
        return self.read(update)[0]['private_channels']

    def getDMIDs(self,update=True): #discord sometimes calls these channel IDs...
        getthatdata = self.read(update) #refreshes session settings if update is True
        return [self.getDMs(False)[i]['id'] for i in range(len(self.getDMs(False)))]

    def getDMData(self,DMID,update=True): #get data about a particular DM
        getthatdata = self.read(update) #refreshes session settings if update is True
        for i in range(len(self.getDMs(False))):
            if self.getDMs(False)[i]['id'] == DMID:
                return self.getDMs(False)[i]
        return None

    def getDMRecipients(self,DMID,update=True): #returns everyone in that DM except your user
        getthatdata = self.read(update) #refreshes session settings if update is True
        return self.getDMData(DMID,False)['recipients']

    #end of DM stuff, heh that wasnt that bad, onto the rest of the stuff

    def getReadStates(self,update=True): #another advantage of using websockets instead of requests (see https://github.com/discord/discord-api-docs/issues/13)
        return self.read(update)[0]['read_state']

    #all about relationships...on discord. note this includes all your friends AND all users youve blocked
    def getRelationships(self,update=True):
        return self.read(update)[0]['relationships']

    def getRelationshipIDs(self,update=True): #gets userIDs that are in a "relationship" with your account
        getthatdata = self.read(update) #refreshes session settings if update is True
        return [self.getRelationships(False)[i]['id'] for i in range(len(self.getRelationships(False)))]

    def getRelationshipData(self,userID,update=True): #usernames and discriminators are no longer provided in this data
        getthatdata = self.read(update) #refreshes session settings if update is True
        for i in range(len(self.getRelationships(False))):
            if self.getRelationships(False)[i]['user_id'] == userID:
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
        return [self.getFriends(False)[i]['user_id'] for i in range(len(self.getFriends(False)))]

    def getBlocked(self,update=True): #nay
        getthatdata = self.read(update) #refreshes session settings if update is True
        blocked = []
        for i in range(len(self.getRelationships(False))):
            if self.getRelationships(False)[i]['type'] == 2:
                blocked.append(self.getRelationships(False)[i])
        return blocked

    def getBlockedIDs(self,update=True):
        getthatdata = self.read(update) #refreshes session settings if update is True
        return [self.getBlocked(False)[i]['user_id'] for i in range(len(self.getBlocked(False)))]

    def getIncomingFriendRequests(self,update=True): #returns data...
        getthatdata = self.read(update) #refreshes session settings if update is True
        ifr = []
        for i in range(len(self.getRelationships(False))):
            if self.getRelationships(False)[i]['type'] == 3:
                ifr.append(self.getRelationships(False)[i])
        return ifr

    def getIncomingFriendRequestIDs(self,update=True):
        getthatdata = self.read(update) #refreshes session settings if update is True
        return [self.getIncomingFriendRequests(False)[i]['user_id'] for i in range(len(self.getIncomingFriendRequests(False)))]

    def getOutgoingFriendRequests(self,update=True):
        getthatdata = self.read(update) #refreshes session settings if update is True
        ofr = []
        for i in range(len(self.getRelationships(False))):
            if self.getRelationships(False)[i]['type'] == 4:
                ofr.append(self.getRelationships(False)[i])
        return ofr

    def getOutgoingFriendRequestIDs(self,update=True):
        getthatdata = self.read(update) #refreshes session settings if update is True
        return [self.getOutgoingFriendRequests(False)[i]['user_id'] for i in range(len(self.getOutgoingFriendRequests(False)))]

    #end of relationship stuff

    def getSessionID(self,update=True):
        return self.read(update)[0]['session_id']

    def getTutorial(self,update=True): #tutorial on what? guess we'll never know...ask discord maybe?
        return self.read(update)[0]['tutorial']

    def getUserData(self,update=True):
        return self.read(update)[0]['user']

    def getUserGuildSettings(self,guildID=None,update=True): #personal settings for a server, like whether or not you want @everyone pings to show, formatting is weird cause you might not want to pass a guildID, hence it is at the end
        getthatdata = self.read(update) #refreshes session settings if update is True
        all_user_guild_settings = self.read(False)[0]['user_guild_settings']
        if guildID != None:
            for i in range(len(all_user_guild_settings)):
                if all_user_guild_settings[i]['guild_id'] == guildID:
                    return all_user_guild_settings[i]
        else:
            return all_user_guild_settings

    def getUserSettings(self,update=True): #returns a class
        return self.read(update)[0]['user_settings']

    def getOptionsForUserSettings(self,update=True):
        return list(self.read(update)[0]['user_settings'].keys())

    def getGeoOrderedRtcRegions(self,update=True):
        return self.read(update)[0]['geo_ordered_rtc_regions']

    def getCachedUsers(self,update=True):
        return self.read(update)[0]['users']

    def getWebsocketVersion(self,update=True):
        return self.read(update)[0]['v']

    # oof end of reading session settings


    '''
    username to snowflake and back. unfortunately, discord's latest build removes some data in session settings, breaking this. Idk I'll prob find a way to fix this later.
    '''
    '''
    def username_to_userID(self,userdiscriminator): #userdiscriminator is "username#discriminator"
        getthatdata = self.read() #might as well get current session settings
        if type(self.getRelationshipData(userdiscriminator,False)).__name__ != 'NoneType': #testing our luck to see if user is in a "relationship" with our user
            return self.getRelationshipData(userdiscriminator,False)['id'] #returns type int
        User(self.discord,self.s,self.log).requestFriend(userdiscriminator) #this puts you in a "relationship" with that user
        if type(self.getRelationshipData(userdiscriminator,True)).__name__ != 'NoneType': #if you sent a request to a bot or to yourself then this becomes False
            User(self.discord,self.s,self.log).removeRelationship(self.getRelationshipData(userdiscriminator,False)['id'])
            return self.getRelationshipData(userdiscriminator,False)['id'] #returns type int
        return None #happens if other user is a bot, is yourself, does not exist, or something wrong with your account

    def userID_to_username(self,userID): #userID aka snowflake
        getthatdata = self.read() #might as well get current session settings
        if type(self.getRelationshipData(userID,False)).__name__ != 'NoneType': #testing our luck to see if user is in a "relationship" with our user
            userdiscriminator = self.getRelationshipData(userID,False)['user']['username'] + "#" + self.getRelationshipData(userID,False)['user']['discriminator']
            return userdiscriminator
        if isinstance(userID,int):
            userID = str(userID)
        User(self.discord,self.s,self.log).requestFriend(userID) #this puts you in a "relationship" with that user
        if type(self.getRelationshipData(userID,True)).__name__ != 'NoneType': #if you sent a request to a bot or to yourself then this becomes False
            User(self.discord,self.s,self.log).removeRelationship(userID)
            userdiscriminator = self.getRelationshipData(userID,False)['user']['username'] + "#" + self.getRelationshipData(userID,False)['user']['discriminator']
            return userdiscriminator
        return None #happens if other user is a bot, is yourself, does not exist, or something wrong with your account
    '''

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

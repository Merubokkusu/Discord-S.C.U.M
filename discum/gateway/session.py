class session:
    settings_ready = {}
    settings_ready_supp = {}
    def __init__(self, input_settings_ready, input_settings_ready_supp):
        session.settings_ready = input_settings_ready
        session.settings_ready_supp = input_settings_ready_supp
        self.guild = guild
        self.DM = DM
        self.relationship = relationship
        self.userGuildSetting = userGuildSetting

    def read(self): #returns all session settings
        return [self.settings_ready, self.settings_ready_supp]

    ###***USER***###
    @property
    def user(self):
        return self.settings_ready['user']

    ###***GUILDS***### (general)
    @property
    def guilds(self):
        return self.settings_ready['guilds']

    @property
    def guildIDs(self):
        return [self.settings_ready['guilds'][i]['id'] for i in range(len(self.settings_ready['guilds']))]

    @property
    def mergedPresences(self):
        return self.settings_ready_supp['merged_presences']['guilds']

    @property
    def positions(self): #outputs your roles, nick, joined at, etc for all guilds you're in
        return self.settings_ready['merged_members']

    def add(self, guilddata):
        self.settings_ready['guilds'].append(guilddata)

    ###***RELATIONSHIPS***### (general)
    @property
    def relationships(self):
        return self.settings_ready['relationships']
    
    @property
    def relationshipIDs(self):
        return [self.relationships[i]['id'] for i in range(len(self.relationships))]

    #friends
    @property
    def friends(self):
        f = []
        for i in range(len(self.relationships)):
            if self.relationships[i]['type'] == 1:
                f.append(self.relationships[i])
        return f
    
    @property
    def friendIDs(self):
        return [self.friends[i]['user_id'] for i in range(len(self.friends))]

    #blocked    
    @property
    def blocked(self):
        b = []
        for i in range(len(self.relationships)):
            if self.relationships[i]['type'] == 2:
                b.append(self.relationships[i])
        return b
    
    @property
    def blockedIDs(self):
        return [self.blocked[i]['user_id'] for i in range(len(self.blocked))]
    
    #incoming    
    @property
    def incomingFriendRequests(self):
        ifr = []
        for i in range(len(self.relationships)):
            if self.relationships[i]['type'] == 3:
                ifr.append(self.relationships[i])
        return ifr
    
    @property
    def incomingFriendRequestIDs(self):
        return [self.incomingFriendRequests[i]['user_id'] for i in range(len(self.incomingFriendRequests))]

    #outgoing
    @property
    def outgoingFriendRequests(self):
        ofr = []
        for i in range(len(self.relationships)):
            if self.relationships[i]['type'] == 4:
                ofr.append(self.relationships[i])
        return ofr
    
    @property
    def outgoingFriendRequestIDs(self):
        return [self.outgoingFriendRequests[i]['user_id'] for i in range(len(self.outgoingFriendRequests))]

    #friend merged presences    
    @property
    def allFriendMergedPresences(self):
        return self.settings_ready_supp['merged_presences']['friends']
    
    @property
    def allFriendMergedPresenceIDs(self):
        return [self.allFriendMergedPresences[i]['user_id'] for i in range(len(self.allFriendMergedPresences))]
        

    ###***DMs***### (general)
    @property
    def DMs(self):
        return self.settings_ready['private_channels']

    @property
    def DMIDs(self):
        return [self.DMs[i]['id'] for i in range(len(self.DMs))] #discord sometimes calls these channel IDs...
        

    ###***USER SETTINGS***### (general)
    @property
    def userGuildSettings(self):
        return self.settings_ready['user_guild_settings'] #personal settings for a server, like whether or not you want @everyone pings to show
    
    @property
    def userSettings(self):
        return self.settings_ready['user_settings']
    
    @property
    def optionsForUserSettings(self):
        return list(self.settings_ready['user_settings'].keys())
        

    ###other stuff
    @property
    def mergedPresences(self):
        return self.settings_ready_supp['merged_presences'] #includes both guild and friend presences, but only the users that are not offline

    @property
    def analyticsToken(self):
        return self.settings_ready['analytics_token']

    @property
    def connectedAccounts(self):
        return self.settings_ready['connected_accounts']

    @property
    def consents(self):
        return self.settings_ready['consents']

    @property
    def experiments(self):
        return self.settings_ready['experiments']

    @property
    def friendSuggestionCount(self):
        return self.settings_ready['friend_suggestion_count']

    @property
    def guildExperiments(self):
        return self.settings_ready['guild_experiments']

    @property
    def readStates(self):
        return self.settings_ready['read_state'] #another advantage of using websockets instead of requests (see https://github.com/discord/discord-api-docs/issues/13)

    @property
    def geoOrderedRtcRegions(self):
        return self.settings_ready['geo_ordered_rtc_regions']

    @property
    def cachedUsers(self):
        return self.settings_ready['users']

    @property
    def tutorial(self):
        return self.settings_ready['tutorial'] #tutorial on what? guess we'll never know...ask discord maybe?


###specific guild
class guild(session):
    def __init__(self, guildID):
        self.guildIndex = None
        for i in range(len(session.settings_ready['guilds'])):
            if session.settings_ready['guilds'][i]['id'] == guildID:
                self.guildIndex = i

    @property
    def data(self):
        return session.settings_ready['guilds'][self.guildIndex]

    def setData(self, newData):
        session.settings_ready['guilds'][self.guildIndex] = newData

    def modify(self, modifications):
        session.settings_ready['guilds'][self.guildIndex].update(modifications)

    @property
    def unavailable(self):
        return 'unavailable' in session.settings_ready['guilds'][self.guildIndex]

    @property
    def hasMembers(self):
        return 'members' in session.settings_ready['guilds'][self.guildIndex]

    @property
    def members(self):
        return session.settings_ready['guilds'][self.guildIndex]['members']

    def resetMembers(self):
        session.settings_ready['guilds'][self.guildIndex]['members'] = {}

    def updateOneMember(self, userID, userProperties):
        session.settings_ready['guilds'][self.guildIndex]['members'][userID] = userProperties

    def updateMembers(self, memberdata): #where member data is a dictionary --> {userId: {properties}}
        session.settings_ready['guilds'][self.guildIndex]['members'].update(memberdata)

    @property
    def owner(self):
        return session.settings_ready['guilds'][self.guildIndex]['owner_id'] #returns type int

    @property
    def boostLvl(self):
        return session.settings_ready['guilds'][self.guildIndex]['premium_tier']

    @property
    def emojis(self):
        return session.settings_ready['guilds'][self.guildIndex]['emojis']

    @property
    def banner(self):
        return session.settings_ready['guilds'][self.guildIndex]['banner'] #if returns 'nil' then there's no banner

    @property
    def discoverySplash(self): #not sure what this is about, something about server discoverability i guess (https://discord.com/developers/docs/resources/guild)
        return session.settings_ready['guilds'][self.guildIndex]['discovery_splash']

    @property
    def msgNotificationSettings(self): #returns an int, 0=all messages, 1=only mentions (https://discord.com/developers/docs/resources/guild#guild-object-default-message-notification-level)
        return session.settings_ready['guilds'][self.guildIndex]['default_message_notifications']

    @property
    def rulesChannelID(self): #nil if no rules channel id, idk if this always works so it might actually be more useful just to look for the word "rules" in channel names
        return session.settings_ready['guilds'][self.guildIndex]['rules_channel_id']

    @property
    def verificationLvl(self): #returns an int, 0-4 (https://discord.com/developers/docs/resources/guild#guild-object-verification-level)
        return session.settings_ready['guilds'][self.guildIndex]['verification_level']

    @property
    def features(self): #returns a list of strings (https://discord.com/developers/docs/resources/guild#guild-object-guild-features)
        return session.settings_ready['guilds'][self.guildIndex]['features']

    @property
    def joinTime(self): #returns when you joined the server, type string
        return session.settings_ready['guilds'][self.guildIndex]['joined_at']

    @property
    def region(self):
        return session.settings_ready['guilds'][self.guildIndex]['region']

    @property
    def applicationID(self): #returns application id of the guild creator if it is bot-created (https://discord.com/developers/docs/resources/guild#guild-object-guild-features)
        return session.settings_ready['guilds'][self.guildIndex]['application_id']

    @property
    def afkChannelID(self): #not sure what this is
        return session.settings_ready['guilds'][self.guildIndex]['afk_channel_id']

    @property
    def icon(self): #https://discord.com/developers/docs/reference#image-formatting
        return session.settings_ready['guilds'][self.guildIndex]['icon']

    @property
    def name(self):
        return session.settings_ready['guilds'][self.guildIndex]['name']

    @property
    def maxVideoChannelUsers(self):
        return session.settings_ready['guilds'][self.guildIndex]['max_video_channel_users']

    @property
    def roles(self): #https://discord.com/developers/docs/topics/permissions#role-object
        return session.settings_ready['guilds'][self.guildIndex]['roles']

    @property
    def publicUpdatesChannelID(self):
        return session.settings_ready['guilds'][self.guildIndex]['public_updates_channel_id']

    @property
    def systemChannelFlags(self): #https://discord.com/developers/docs/resources/guild#guild-object-system-channel-flags
        return session.settings_ready['guilds'][self.guildIndex]['system_channel_flags']

    @property
    def mfaLvl(self): #https://discord.com/developers/docs/resources/guild#guild-object-mfa-level
        return session.settings_ready['guilds'][self.guildIndex]['mfa_level']

    @property
    def afkTimeout(self): #returns type int, unit seconds, https://discord.com/developers/docs/resources/guild
        return session.settings_ready['guilds'][self.guildIndex]['afk_timeout']

    @property
    def hashes(self): #https://github.com/discord/discord-api-docs/issues/1642
        return session.settings_ready['guilds'][self.guildIndex]['guild_hashes']

    @property
    def systemChannelID(self): #returns an int, the id of the channel where guild notices such as welcome messages and boost events are posted
        return session.settings_ready['guilds'][self.guildIndex]['system_channel_id']

    @property
    def lazy(self): #slightly different naming format since it returns a boolean (https://luna.gitlab.io/discord-unofficial-docs/lazy_guilds.html)
        if session.settings_ready['guilds'][self.guildIndex]['lazy'] == 'true':
            return True
        else:
            return False

    @property
    def numBoosts(self): #get number of boosts the server has gotten
        return session.settings_ready['guilds'][self.guildIndex]['premium_subscription_count']

    @property
    def large(self): #slightly different naming format since it returns a boolean, large if more than 250 members
        if session.settings_ready['guilds'][self.guildIndex]['large'] == 'true':
            return True
        else:
            return False

    @property
    def explicitContentFilter(self): #https://discord.com/developers/docs/resources/guild#guild-object-explicit-content-filter-level
        return session.settings_ready['guilds'][self.guildIndex]['explicit_content_filter']

    @property
    def splashHash(self): #not sure what this is for
        return session.settings_ready['guilds'][self.guildIndex]['splash']

    @property
    def memberCount(self):
        return session.settings_ready['guilds'][self.guildIndex]['member_count']

    @property
    def description(self):
        return session.settings_ready['guilds'][self.guildIndex]['description']

    @property
    def vanityUrlCode(self):
        return session.settings_ready['guilds'][self.guildIndex]['vanity_url_code']

    @property
    def preferredLocale(self):
        return session.settings_ready['guilds'][self.guildIndex]['preferred_locale']

    @property
    def allChannels(self): #returns all categories and all channels, all the data about that, wall of data so it can be a bit overwhelming, useful if you want to check how many channels your server has since discord counts categories as channels
        return session.settings_ready['guilds'][self.guildIndex]['channels']

    @property
    def categories(self): #all data about all guild categories, can be overwhelming
        all_channels = session.settings_ready['guilds'][self.guildIndex]['channels']
        all_categories = []
        for channel in all_channels: #https://discord.com/developers/docs/resources/channel#channel-object-channel-types
            if channel['type'] == 4:
                all_categories.append(channel)
        return all_categories

    @property
    def categoryIDs(self):
        return [self.categories[i]['id'] for i in range(len(self.categories))]

    def categoryData(self,categoryID):
        for i in range(len(self.categories)):
            if self.categories[i]['id'] == categoryID:
                return self.categories[i]
        return None #category not found

    @property
    def channels(self): #all data about all guild channels, can be overwhelming
        all_channels = session.settings_ready['guilds'][self.guildIndex]['channels']
        all_non_categories = []
        for channel in all_channels: #https://discord.com/developers/docs/resources/channel#channel-object-channel-types
            if channel['type'] != 4:
                all_non_categories.append(channel)
        return all_non_categories

    @property
    def channelIDs(self):
        return [self.channels[i]['id'] for i in range(len(self.channels))]

    def channelData(self,channelID):
        for i in range(len(self.channels)):
            if self.channels[i]['id'] == channelID:
                return self.channels[i]
        return None #channel not found

    @property
    def voiceStates(self): #https://discord.com/developers/docs/resources/voice#voice-state-object
        return session.settings_ready_supp['guilds'][self.guildIndex]['voice_states']

    @property
    def notOfflineCachedMembers(self): #so, not offline, but not all the not-offline members so....not offline cached members. I know I know long function name, but it's descriptive.
        return session.settings_ready_supp['merged_members'][self.guildIndex]

    @property
    def notOfflineCachedMemberIDs(self):
        return [self.notOfflineCachedMembers[i]['user_id'] for i in range(len(self.notOfflineCachedMembers))]

    def notOfflineCachedMemberData(self,userID):
        for i in range(len(self.notOfflineCachedMembers)):
            if self.notOfflineCachedMembers[i]['user_id'] == userID:
                return self.notOfflineCachedMembers[i]
        return None

    @property
    def mergedPresences(self): #this is different from getGuildNotOfflineCachedMembers because you can see presence data. also, not sure why, but a diff number of members shows up here than getGuildNotOfflineCachedMembers
        return session.settings_ready_supp['merged_presences']['guilds'][self.guildIndex]

    @property
    def mergedPresenceIDs(self): #returns user ids in a list
        return [self.mergedPresences[i]['user_id'] for i in range(len(self.mergedPresences))]

    def mergedPresenceData(self,userID):
        for i in range(len(self.mergedPresences)):
            if self.mergedPresences[i]['user_id'] == userID:
                return self.mergedPresences[i]
        return None

    @property
    def position(self): #my roles in guild and other data
        return session.settings_ready['merged_members'][self.guildIndex]

###specific relationship
class relationship(session): #not the same organization as class guild
    def __init__(self, userID):
        self.userID = userID

    @property
    def data(self): #usernames and discriminators are no longer provided in this data
        for i in range(len(session.settings_ready['relationships'])):
            if session.settings_ready['relationships'][i]['user_id'] == self.userID:
                return session.settings_ready['relationships'][i]
        return None

    @property
    def friendMergedPresenceData(self):
        for i in range(len(session.settings_ready_supp['merged_presences']['friends'])):
            if session.settings_ready_supp['merged_presences']['friends'][i]['user_id'] == self.userID:
                return session.settings_ready_supp['merged_presences']['friends'][i]
        return None

###specific DM
class DM(session):
    def __init__(self, DMID):
        self.DMID = DMID

    @property
    def data(self):
        for i in range(len(session.settings_ready['private_channels'])):
            if session.settings_ready['private_channels'][i]['id'] == self.DMID:
                return session.settings_ready['private_channels'][i]
        return None

    @property
    def recipients(self): #returns everyone in that DM except you
        return self.data['recipient_ids']

###specific User Guild Settings
class userGuildSetting(session):
    def __init__(self, guildID):
        self.guildID = guildID

    @property
    def data(self):
        if len(session.settings_ready['user_guild_settings']['entries']) == 0:
            return None
        for i in range(len(session.settings_ready['user_guild_settings']['entries'])):
            if session.settings_ready['user_guild_settings']['entries'][i]['guild_id'] == self.guildID:
                return session.settings_ready['user_guild_settings']['entries'][i]
        return None

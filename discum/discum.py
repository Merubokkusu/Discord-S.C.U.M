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

class Client:
    def __init__(self, email="none", password="none", token="none", proxy_host=None, proxy_port=None, user_agent="random", log=True): #not using None on email pass and token since that could get flagged by discord...
        self.log = log
        self.__user_token = token
        self.__user_email = email
        self.__user_password = password
        self.__proxy_host = proxy_host
        self.__proxy_port = proxy_port
        self.session_settings = {} #look at function read()
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
        if self.__user_token == "none": #assuming email and pass are given...
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
    def read(self,update=True): #returns a class, this is the main function, if you want ALL the session data (wall of data), then call this (or bot.read().__dict__). if update=False session_settings will not be updated
        if update == False: #if read() hasnt been called yet this will just return an empty dict
            return self.session_settings
        self.__gateway_server.run('get session data',log=self.log)
        self.session_settings = self._Client__gateway_server.session_data["d"]
        return self.session_settings

    def getAnalyticsToken(self,update=True):
    	return self.read(update)['analytics_token']

    def getConnectedAccounts(self,update=True):
    	return self.read(update)['connected_accounts']

    def getConsents(self,update=True):
    	return self.read(update)['consents']

    def getExperiments(self,update=True):
    	return self.read(update)['experiments']

    def getFriendSuggestionCount(self,update=True): #no idea what this is but it's here so whatever
    	return self.read(update)['friend_suggestion_count']

    def getGuildExperiments(self,update=True):
    	return self.read(update)['guild_experiments']


    #Some info about guilds...discord's latest build has removed a lot of guild info from session settings
    def getGuilds(self,update=True): 
    	return self.read(update)['guilds']

    def getGuildIDs(self,update=True): #just get the guild ids, type list
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	return [self.getGuilds(False)[i]['id'] for i in range(len(self.getGuilds(False)))]

    def getGuildVoiceStates(self,guildID,update=True): #https://discord.com/developers/docs/resources/voice#voice-state-object
        getthatdata = self.read(update) #refreshes session settings if update is True
        guildIndex = self.getGuildIDs(False).index(guildID)
        return self.getGuilds(False)[guildIndex]['voice_states']

    def getGuildCachedMembers(self,guildID,update=True): #all data about all cached members a guild you're in
        getthatdata = self.read(update) #refreshes session settings if update is True
        guildIndex = self.getGuildIDs(False).index(guildID)
        return self.getGuildData(guildID,False)[guildIndex]

    def getGuildCachedMemberIDs(self,guildID,update=True):
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	return [self.getGuildMembers(guildID,False)[i]['user_id'] for i in range(len(self.getGuildMembers(guildID,False)))]

    def getGuildCachedMemberData(self,guildID,userID,update=True):
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	for i in range(len(self.getGuildMembers(guildID,False))):
    		if self.getGuildMembers(guildID,False)[i]['user_id'] == userID:
    			return self.getGuildMembers(guildID,False)[i]
    	return None

    # end of guild stuff, now onto the other stuff

    def getCachedFriends(self,update=True):
        return self.read(update)['merged_presences']['friends']

    def getNotes(self,update=True):
    	return self.read(update)['notes'] #returns a dict where the keys are user IDs and the values are the notes

    def getOnlineFriends(self,update=True): #i saw no reason to make "sub functions" of this since it's only about online friends
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	return self.read(False)['presences']

    #all about DMs, aw geez this is gonna be a long one too i guess...
    def getDMs(self,update=True):
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	return self.read(False)['private_channels']

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
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	return self.read(False)['read_state']

    #all about relationships...on discord. note this includes all your friends AND all users youve blocked
    def getRelationships(self,update=True):
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	return self.read(False)['relationships']

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
    	return self.read(update)['session_id']

    def getTutorial(self,update=True): #tutorial on what? guess we'll never know...ask discord maybe?
    	return self.read(update)['tutorial']

    def getUserData(self,update=True):
    	return self.read(update)['user']

    def getUserGuildSettings(self,guildID=None,update=True): #personal settings for a server, like whether or not you want @everyone pings to show, formatting is weird cause you might not want to pass a guildID, hence it is at the end
    	getthatdata = self.read(update) #refreshes session settings if update is True
    	all_user_guild_settings = self.read(False).user_guild_settings
    	if guildID != None:
    		for i in range(len(all_user_guild_settings)):
    			if all_user_guild_settings[i]['guild_id'] == guildID:
    				return all_user_guild_settings[i]
    	else:
    		return all_user_guild_settings

    def getUserSettings(self,update=True): #returns a class
    	return self.read(update)['user_settings']

    def getOptionsForUserSettings(self,update=True):
    	return list(self.read(update)['user_settings'].keys())

    def getWebsocketVersion(self,update=True):
    	return self.read(update)['v']

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
    def getMessages(self,channelID,num=1,beforeDate=None): # num <= 100, beforeDate is a snowflake
        return Messages(self.discord,self.s,self.log).getMessages(channelID,num,beforeDate)

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

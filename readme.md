### A Discord Selfbot Api - discum

![https://files.catbox.moe/3ns003.png](https://files.catbox.moe/3ns003.png)

[![PyPI version](https://badge.fury.io/py/discum.svg)](https://badge.fury.io/py/discum)


## Install
from PyPI:      
```python
pip install discum 
```
     
from source (this is up-to-date with recent changes)(currently on version 0.2.0):        
`git clone https://github.com/Merubokkusu/Discord-S.C.U.M.git`    
`cd Discord-S.C.U.M`     
`python3 setup.py install`                   

# Usage
## [Read the Wiki](https://github.com/Merubokkusu/Discord-S.C.U.M/wiki)

# Example
```python
import discum     
bot = discum.Client(email=,password=)
#bot = discum.Client(email=,password=,proxy_host=,proxy_port=)
#bot = discum.Client(token=)
bot.read()
bot.read(update=False).__dict__
bot.getGuildIDs(update=False)
bot.sendMessage("383003333751856129","Hello You :)")
```

### bonus features: 
convert username to userID and back:
```python
bot.username_to_userID(userdiscriminator) #input is "username#discriminator". you cannot input bot accounts or yourself
bot.userID_to_username(snowflake) #input is userID (aka snowflake). you cannot input bot accounts or yourself
```
convert unix timestamp to snowflake and back:
```python
bot.unixts_to_snowflake(unixts) #unixts is of type int
bot.snowflake_to_unixts(snowflake) #snowflake is of type int
```

### want to extract all messages ever sent in a server?
```python
bot.getMessages(guildID) #returns type dict
```
\*note: wouldn't recommend running this on really active servers (~200 msgs per 15 seconds) because this command might never finish running.    
time between each request defaults to 1 second, if you want to change this do `bot.getMessages(guildID,waitTime=0)` or whatever other number of seconds you want.   
if you set waitTime to 0 you will get rate limited (every 40 or so requests) and you'll have to wait about 40 seconds.      


# To Do
- [x] Sending basic text messages
- [X] Sending Images
- [x] Sending Embeds
- [X] Sending Requests (Friends etc)
- [X] Profile Editing (Name,Status,Avatar)
- [ ] Making phone calls, sending audio/video data thru those calls
- [ ] Everything

# list of all functions (click thru these and github should show their location in discum.py)
```python
discum.Client(email="none", password="none", token="none", proxy_host=False, proxy_port=False) #look at __init__
snowflake_to_unixts(self,snowflake)
unixts_to_snowflake(self,unixts)
read(self,update=True)
getAnalyticsToken(self,update=True)
getConnectedAccounts(self,update=True)
getConsents(self,update=True)
getExperiments(self,update=True)
getFriendSuggestingCount(self,update=True)
getGuildExperiments(self,update=True)
getGuilds(self,update=True)
getGuildIDs(self,update=True)
getGuildData(self,guildID,update=True)
getGuildOwner(self,guildID,update=True)
getGuildBoostLvl(self,guildID,update=True)
getGuildEmojis(self,guildID,update=True)
getGuildBanner(self,guildID,update=True)
getGuildDiscoverySplash(self,guildID,update=True): #not sure what this is about, something about server discoverability i guess (https
getGuildUserPresences(self,guildID,update=True)
getGuildMsgNotificationSettings(self,guildID,update=True): #returns an int, 0=all messages, 1=only mentions (https
getGuildRulesChannelID(self,guildID,update=True)
getGuildVerificationLvl(self,guildID,update=True): #returns an int, 0-4 (https
getGuildFeatures(self,guildID,update=True): #returns a list of strings (https
getGuildJoinTime(self,guildID,update=True)
getGuildRegion(self,guildID,update=True)
getGuildApplicationID(self,GuildID,update=True): #returns application id of the guild creator if it is bot-created (https
getGuildAfkChannelID(self,guildID,update=True)
getGuildIcon(self,guildID,update=True): #https
getGuildName(self,guildID,update=True)
getGuildMaxVideoChannelUsers(self,guildID,update=True)
getGuildRoles(self,guildID,update=True): #https
getGuildPublicUpdatesChannelID(self,guildID,update=True)
getGuildSystemChannelFlags(self,guildID,update=True): #https
getGuildMfaLvl(self,guildID,update=True): #https
getGuildAfkTimeout(self,guildID,update=True): #returns type int, unit seconds, https
getGuildHashes(self,guildID,update=True): #https
getGuildSystemChannelID(self,guildID,update=True)
isGuildLazy(self,guildID,update=True): #slightly different naming format since it returns a boolean (https
getGuildNumBoosts(self,guildID,update=True)
isGuildLarge(self,guildID,update=True)
getGuildExplicitContentFilter(self,guildID,update=True): #https
getGuildSplashHash(self,guildID,update=True)
getGuildVoiceStates(self,guildID,update=True): #https
getGuildMemberCount(self,guildID,update=True)
getGuildDescription(self,guildID,update=True)
getGuildVanityUrlCode(self,guildID,update=True)
getGuildPreferredLocale(self,guildID,update=True)
getGuildAllChannels(self,guildID,update=True)
getGuildCategories(self,guildID,update=True)
getGuildCategoryIDs(self,guildID,update=True)
getGuildCategoryData(self,guildID,categoryID,update=True)
getGuildChannels(self,guildID,update=True)
getGuildChannelIDs(self,guildID,update=True)
getGuildChannelData(self,guildID,channelID,update=True)
getGuildMembers(self,guildID,update=True)
getGuildMemberIDs(self,guildID,update=True)
getGuildMemberData(self,guildID,memberID,update=True)
getNotes(self,update=True)
getOnlineFriends(self,update=True)
getDMs(self,update=True)
getDMIDs(self,update=True)
getDMData(self,DMID,update=True)
getDMRecipients(self,DMID,update=True)
getReadStates(self,update=True): #another advantage of using websockets instead of requests (see https
getRelationships(self,update=True)
getRelationshipIDs(self,update=True)
getRelationshipData(self,RelationshipID,update=True)
getFriends(self,update=True)
getFriendIDs(self,update=True)
getBlocked(self,update=True)
getBlockedIDs(self,update=True)
getIncomingFriendRequests(self,update=True)
getIncomingFriendRequestIDs(self,update=True)
getOutgoingFriendRequests(self,update=True)
getOutgoingFriendRequestIDs(self,update=True)
getSessionID(self,update=True)
getTutorial(self,update=True)
getUserData(self,update=True)
getUserGuildSettings(self,update=True,guildID=None)
getUserSettings(self,update=True)
getOptionsForUserSettings(self,update=True)
getWebsocketVersion(self,update=True)
username_to_userID(self,userdiscriminator)
userID_to_username(self,userID)
getMessages(self,guildID,channelID=None,userID=None,mentionsUserID=None,has=None,beforeDate=None,afterDate=None,textSearch=None)
getRecentMessage(self,channelID,num=1)
sendMessage(self,channelID,message,embed="",tts=False)
sendFile(self,channelID,filelocation,isurl=False,message="")
requestFriend(self,user)
acceptFriend(self,userID)
removeRelationship(self,userID)
blockUser(self,userID)
changeName(self,name)
setStatus(self,status)
setAvatar(self,imagePath)
```

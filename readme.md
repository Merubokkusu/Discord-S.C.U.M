### A Discord Selfbot Api - discum

![https://files.catbox.moe/3ns003.png](https://files.catbox.moe/3ns003.png)

[![PyPI version](https://badge.fury.io/py/discum.svg)](https://badge.fury.io/py/discum)


## Install
from PyPI (OUTDATED):      
```python
pip install discum 
```
     
from source (this is up-to-date with recent changes)(currently on version 0.2.1):        
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

### want to extract all messages ever sent in a server? (includes search function)
```python
bot.getMessages(guildID) #returns type dict
```
* \*note: for highly active servers (>500 messages every 30 seconds or so) you might need to set the beforeDate so that getMessages doesnt run literally forever
* time between each request defaults to 1 second, if you want to change this do `bot.getMessages(guildID,waitTime=0)` or whatever other number of seconds you want.       
* if you set waitTime to 0 you will get rate limited (every 40 or so requests) and you'll have to wait about 40 seconds.      
* input types for the search feature: 
  * channelID,userID,mentionsUserID are lists of either ints or strings
  * has is a list of strings
  * beforeDate and afterDate are ints
  * textSearch is a string
  * waitTime is an int or double

##### on that note, the normal way to get messages (≤ last 100 messages, before a date, in a channel):
```python
bot.getRecentMessage(channelID,num=100)
```

# To Do
- [x] Sending basic text messages
- [X] Sending Images
- [x] Sending Embeds
- [X] Sending Requests (Friends etc)
- [X] Profile Editing (Name,Status,Avatar)
- [ ] Making phone calls, sending audio/video data thru those calls
- [ ] Everything

# list of all 101 functions (click thru these and github should show their location in discum.py)
```python
discum.Client(email="none", password="none", token="none", proxy_host=False, proxy_port=False) #look at __init__
snowflake_to_unixts(snowflake)
unixts_to_snowflake(unixts)
read(update=True)
getAnalyticsToken(update=True)
getConnectedAccounts(update=True)
getConsents(update=True)
getExperiments(update=True)
getFriendSuggestingCount(update=True)
getGuildExperiments(update=True)
getGuilds(update=True)
getGuildIDs(update=True)
getGuildData(guildID,update=True)
getGuildOwner(guildID,update=True)
getGuildBoostLvl(guildID,update=True)
getGuildEmojis(guildID,update=True)
getGuildBanner(guildID,update=True)
getGuildDiscoverySplash(guildID,update=True): #not sure what this is about, something about server discoverability i guess (https
getGuildUserPresences(guildID,update=True)
getGuildMsgNotificationSettings(guildID,update=True): #returns an int, 0=all messages, 1=only mentions (https
getGuildRulesChannelID(guildID,update=True)
getGuildVerificationLvl(guildID,update=True): #returns an int, 0-4 (https
getGuildFeatures(guildID,update=True): #returns a list of strings (https
getGuildJoinTime(guildID,update=True)
getGuildRegion(guildID,update=True)
getGuildApplicationID(GuildID,update=True): #returns application id of the guild creator if it is bot-created (https
getGuildAfkChannelID(guildID,update=True)
getGuildIcon(guildID,update=True): #https
getGuildName(guildID,update=True)
getGuildMaxVideoChannelUsers(guildID,update=True)
getGuildRoles(guildID,update=True): #https
getGuildPublicUpdatesChannelID(guildID,update=True)
getGuildSystemChannelFlags(guildID,update=True): #https
getGuildMfaLvl(guildID,update=True): #https
getGuildAfkTimeout(guildID,update=True): #returns type int, unit seconds, https
getGuildHashes(guildID,update=True): #https
getGuildSystemChannelID(guildID,update=True)
isGuildLazy(guildID,update=True): #slightly different naming format since it returns a boolean (https
getGuildNumBoosts(guildID,update=True)
isGuildLarge(guildID,update=True)
getGuildExplicitContentFilter(guildID,update=True): #https
getGuildSplashHash(guildID,update=True)
getGuildVoiceStates(guildID,update=True): #https
getGuildMemberCount(guildID,update=True)
getGuildDescription(guildID,update=True)
getGuildVanityUrlCode(guildID,update=True)
getGuildPreferredLocale(guildID,update=True)
getGuildAllChannels(guildID,update=True)
getGuildCategories(guildID,update=True)
getGuildCategoryIDs(guildID,update=True)
getGuildCategoryData(guildID,categoryID,update=True)
getGuildChannels(guildID,update=True)
getGuildChannelIDs(guildID,update=True)
getGuildChannelData(guildID,channelID,update=True)
getGuildMembers(guildID,update=True)
getGuildMemberIDs(guildID,update=True)
getGuildMemberData(guildID,memberID,update=True)
getNotes(update=True)
getOnlineFriends(update=True)
getDMs(update=True)
getDMIDs(update=True)
getDMData(DMID,update=True)
getDMRecipients(DMID,update=True)
getReadStates(update=True): #another advantage of using websockets instead of requests (see https
getRelationships(update=True)
getRelationshipIDs(update=True)
getRelationshipData(RelationshipID,update=True)
getFriends(update=True)
getFriendIDs(update=True)
getBlocked(update=True)
getBlockedIDs(update=True)
getIncomingFriendRequests(update=True)
getIncomingFriendRequestIDs(update=True)
getOutgoingFriendRequests(update=True)
getOutgoingFriendRequestIDs(update=True)
getSessionID(update=True)
getTutorial(update=True)
getUserData(update=True)
getUserGuildSettings(update=True,guildID=None)
getUserSettings(update=True)
getOptionsForUserSettings(update=True)
getWebsocketVersion(update=True)
username_to_userID(userdiscriminator)
userID_to_username(userID)
getMessages(guildID,channelID=None,userID=None,mentionsUserID=None,has=None,beforeDate=None,afterDate=None,textSearch=None,waitTime=1)
getRecentMessage(channelID,num=1,beforeDate=None)
sendMessage(channelID,message,embed="",tts=False)
sendFile(channelID,filelocation,isurl=False,message="")
searchMessages(guildID,channelID=None,userID=None,mentionsUserID=None,has=None,beforeDate=None,afterDate=None,textSearch=None,afterNumResults=None)
typingAction(channelID)
deleteMessage(channelID,messageID)
pinMessage(channelID,messageID)
unPinMessage(channelID,messageID)
getPins(channelID)
requestFriend(user)
acceptFriend(userID)
removeRelationship(userID)
blockUser(userID)
changeName(name)
setStatus(status)
setAvatar(imagePath)
```

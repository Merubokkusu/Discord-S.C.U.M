### A Discord Selfbot Api - discum

![https://files.catbox.moe/3ns003.png](https://files.catbox.moe/3ns003.png)

[![PyPI version](https://badge.fury.io/py/discum.svg)](https://badge.fury.io/py/discum)


## Install
from PyPI:      
```python
pip install discum 
```
     
from source (this is up-to-date with recent changes)(currently on version 0.2.2):        
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

## What's new in v 0.2.2:
greatly simplified and improved GatewayServer protocol & ability to send custom data to Discord via websockets:    
The following initiates a call with a friend and stops the asyncio loop once a message is recieved with event name VOICE_SERVER_UPDATE. Note that you'll need to send a different message to the server to hang up the call.
```python
bot.__gateway_server.runIt({
  1: {
    "send": [{
      "op": 4,
      "d": {
        "guild_id": None,
        "channel_id": 21154535154122752,
        "self_mute": False,
        "self_deaf": False,
        "self_video": False
      }
    }],
    "receive": [{
      "t": "VOICE_SERVER_UPDATE"
    }]
  }
})
```
The input for \_\_gateway_server.runIt is formatted like such:
```
{
  1: {
    "send": [{}, {}, {}],
    "receive": [{}]
  },
  2: {
    "send": [{}],
    "receive": [{}, {}]
  }
}
```
tasks are placed in sequencial order (note the 1 and the 2) and are run as such. The 2nd task does not start running until the 1st task has been completed. Each task has "send" and "recieve" sections.      
The send section denotes what data to send to the server, and it's value is a list of dicts (https://discord.com/developers/docs/topics/gateway). If there are multiple messages to send to the server, each message will be sent before the "receive" section is checked.     
The receive section (a list of dicts) acts like a search function and looks like this: 
```
{
  "op": (optional; type int),
  "d": {
    "key": (optional; type str or int),
    "value": (optional; no set type),
    "text": (optional; type str)
  },
  "s": (optional; type int),
  "t": (optional; type str)
}
```
As an example, if you'd like to connect to Discord via websockets and never disconnect, run the following:
```
bot.__gateway_server.runIt({
  1: {
    "send": [],
    "receive": []
  }
})
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
getFriendSuggestionCount(update=True)
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
getMessages(channelID,num=1,beforeDate=None)
sendMessage(channelID,message,embed="",tts=False)
sendFile(channelID,filelocation,isurl=False,message="")
searchMessages(guildID,channelID=None,userID=None,mentionsUserID=None,has=None,beforeDate=None,afterDate=None,textSearch=None,afterNumResults=None)
filterSearchResults(searchResponse)
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

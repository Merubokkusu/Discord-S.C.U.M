![version](https://img.shields.io/badge/version-0.2.5-blue) [![PyPI version](https://badge.fury.io/py/discum.svg)](https://badge.fury.io/py/discum) [![python versions](https://img.shields.io/badge/python-3.7%20%7C%203.8-blue)](https://pypi.org/project/discum/0.2.1/) [![Downloads](https://pepy.tech/badge/discum/month)](https://pepy.tech/project/discum/month) [![Gitter chat](https://badges.gitter.im/discum/gitter.png)](https://gitter.im/discum/community)


### A Discord Selfbot Api Wrapper - discum

![https://files.catbox.moe/3ns003.png](https://files.catbox.moe/3ns003.png)

\* [changelog](https://github.com/Merubokkusu/Discord-S.C.U.M/blob/master/changelog.md). Updates are slow nowadays due to school and covid and life.
## Info
  Discum is a Discord selfbot api wrapper (in case you didn't know, selfbotting = automating a user account). Whenever you login to discord, your client communicates with Discord's servers using Discord's http api (http(s) requests) and gateway server (websockets). Discum allows you have this communication with Discord with python. 
  
  The main difference between Discum and other Discord api wrapper libraries (like discord.py) is that discum is written and maintained to work on user accounts (so, perfect for selfbots). We thoroughly test all code on here and develop discum to be readable, expandable, and useable.     
  
  Note, using a selfbot is against Discord's Terms of Service and you could get banned for using one if you're not careful. Also, this needs to be said: discum does not have rate limit handling. The main reasons for this are that discum is made to (1) be (relatively) simple and (2) give the developer/user freedom (generally I'd recommend a bit more than 1 second in between tasks of the same type, but if you'd like a longer or shorter wait time that's up to you). We (Merubokkusu and anewrandomaccount) do not take any responsibility for any consequences you might face while using discum. We also do not take any responsibility for any damage caused (to servers/channels) through the use of Discum. Discum is a tool; how you use this tool is on you.

## Install (installation should be the same on Mac, Linux, Windows, etc; just make sure you're using python 3.7 or 3.8)
from PyPI (this is probably outdated, installing from source is recommended):      
```python
pip install discum 
```
     
from source (this is up-to-date with recent changes)(currently on version 0.2.5):      
```
git clone https://github.com/Merubokkusu/Discord-S.C.U.M.git
cd Discord-S.C.U.M
python3 setup.py install               
```

# Usage
### [Read the Wiki](https://github.com/Merubokkusu/Discord-S.C.U.M/blob/master/wiki.md)

# Example
```python
import discum     
bot = discum.Client(email=,password=) #note, this will not work if you have a MFA account
#bot = discum.Client(email=,password=,proxy_host=,proxy_port=,user_agent=)
#bot = discum.Client(email=,password=,token=) #works for all types of accounts
#bot = discum.Client(token=) #works for all types of accounts, no profile editing however
#bot = discum.Client(token=,proxy_host=,proxy_port=) #works for all types of accounts, no profile editing however
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
discum.Client(email="none", password="none", token="none", proxy_host=False, proxy_port=False, user_agent="random") #look at __init__
connectionTest()
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
getMessages(channelID,num=1,beforeDate=None)
createDM(userIDs) #userIDs is a list of (str) user IDs. Even if it's just 1 user id, it's still in list format.
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
_Client__gateway_server.runIt(data) #for websocket connections
getInfoFromInviteCode(inviteCode)
joinGuild(inviteCode)
kick(guildID,userID,reason="")
ban(guildID,userID,deleteMessagesDays,reason="")
```

### notes:
arandomnewaccount here - my profile is invisible because this isn't my only github account and therefore I've been marked as spam by github. I'll still be commiting onto the repo from time to time but I won't be able to answer issues on the issue page. If you want to contact me about discum (issues, questions, etc) you can send an email to discordtehe@gmail.com.

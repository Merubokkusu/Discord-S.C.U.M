![version](https://img.shields.io/badge/version-0.2.4-blue) [![PyPI version](https://badge.fury.io/py/discum.svg)](https://badge.fury.io/py/discum) [![python versions](https://img.shields.io/badge/python-3.7%20%7C%203.8-blue)](https://pypi.org/project/discum/0.2.1/) [![Downloads](https://pepy.tech/badge/discum/month)](https://pepy.tech/project/discum/month) [![Gitter chat](https://badges.gitter.im/discum/gitter.png)](https://gitter.im/discum/community)


### A Discord Selfbot Api Wrapper - discum

![https://files.catbox.moe/3ns003.png](https://files.catbox.moe/3ns003.png)

\* scroll to the bottom for changelog
## Info
  Discum is a Discord selfbot api wrapper (in case you didn't know, selfbotting = automating a user account). Whenever you login to discord, your client communicates with Discord's servers using Discord's http api (http(s) requests) and gateway server (websockets). Discum allows you communicate with Discord using python. 
  
  The main difference between Discum and other Discord api wrapper libraries (like discord.py) is that discum is written and maintained to work on user accounts (so, perfect for selfbots). We thoroughly test all code on here and develop discum to be readable, expandable, and useable.     
  
  Note, using a selfbot is against Discord's Terms of Service and you could get banned for using one if you're not careful. We (Merubokkusu and anewrandomaccount) do not take any responsibility for any consequences you might face while using discum.       

## Install (installation should be the same on Mac, Linux, Windows, etc; just make sure you're using python 3.7 or 3.8)
from PyPI:      
```python
pip install discum 
```
     
from source (this is up-to-date with recent changes)(currently on version 0.2.4):      
```
git clone https://github.com/Merubokkusu/Discord-S.C.U.M.git
cd Discord-S.C.U.M
python3 setup.py install               
```

# Usage
## [Read the Wiki](https://github.com/Merubokkusu/Discord-S.C.U.M/wiki)

# Example
```python
import discum     
bot = discum.Client(email=,password=) #note, this will not work if you have a MFA account
#bot = discum.Client(email=,password=,proxy_host=,proxy_port=)
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

# list of all 103 functions (click thru these and github should show their location in discum.py)
```python
discum.Client(email="none", password="none", token="none", proxy_host=False, proxy_port=False) #look at __init__
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
_Client__gateway_server.runIt(data) #for websocket connections
```

### notes:
arandomnewaccount here - my profile is invisible because this isn't my only github account and therefore I've been marked as spam by github. I'll still be commiting onto the repo from time to time but I won't be able to answer issues on the issue page. If you want to contact me about discum (issues, questions, etc) you can send an email to discordtehe@gmail.com.

# Changelog
# 0.2.4
### Changed
- task receive checking (in gateway/GatewayServer.py) for better searching thru nested dictionaries. see the following example for getting the members of a server that has a little over 300 members:
  ```python
  bot._Client__gateway_server.runIt({
    1: {
      "send": [{
        "op": 14,
        "d": {
          "guild_id": "705058712922095646",
          "channels": {
            "705060010111139860": [
              [0, 99],
              [100, 199]
            ]
          }
        }
      }],
      "receive": [{
        "keyvaluechecker": [
          ['d', 'ops', 0, 'range'],
          [100, 199]
        ]
      }]
    },
    2: {
      "send": [{
        "op": 14,
        "d": {
          "guild_id": "705058712922095646",
          "channels": {
            "705060010111139860": [
              [200, 299],
              [300, 399]
            ]
          }
        }
      }],
      "receive": [{
        "keychecker": ['d', 'ops', 0, 'range']
      }]
    }
  })
  ```
  As you can see above, the receive format has changed to allow this. This is the new receive format:
  ```
  {
  "op": (optional; type int),
  "d": {
    "keys": (optional; type list of strings),
    "values": (optional; list of no set types),
    "texts": (optional; type list of strings)
  },
  "s": (optional; type int),
  "t": (optional; type str),
  "keychecker": (optional; type list),
  "keyvaluechecker": (optional; type list)
  }
  ```
  And...here's how to use the receive format above:
  ```
  {
  "op": integer,
  "d": {
    "keys": [depth 1 keys (in any order) of receivedmessage["d"]],
    "values": [depth 1 values (in any order) of receivedmessage["d"]],
    "texts": [a bunch of strings looks through str(receivedmessage["d"])]
  },
  "s": integer,
  "t": string,
  "keychecker": ["list","of","keys","in","the","order","which","they","are","nested","in"],
  "keyvaluechecker": [["list","of","keys","in","the","order","which","they","are","nested","in"],"value to check for"]
  }
  ```
  Note, both keychecker and keyvaluechecker accept integers in certain situations. For example, if the received dictionary had a list of dictionaries as one of its values. See the example for getting members above.
# 0.2.3
### Changed
- structure of code: all gateway comms are now in the gateway folder, Login.py is now in the login folder
- variable names in gateway/GatewayServer.py to improve code readability (+ added more comments)
- task receive checking (in gateway/GatewayServer.py) to allow more flexibility (you don't have to search for the last received message in a batch of messages anymore. now you just search messages. like normal.). Here's an example use case:
  ```python
  bot._Client__gateway_server.runIt({
    1: {
      "send": [{
        "op": 4,
        "d": {
          "guild_id": None,
          "channel_id": CHANNEL_ID,
          "self_mute": False,
          "self_deaf": False,
          "self_video": False
        }
      }],
      "receive": [
        {"t": "VOICE_SERVER_UPDATE"}, 
        {"t": "VOICE_STATE_UPDATE"}
      ]
    }
  })
  ```
  note that the order of the receive values do not matter. Whether or not VOICE_STATE_UPDATE comes second (it actually comes first) doesn't matter.
- receive inputs slightly changed to allow for more checking possibilities. Now the format is like such:
  ```
  {
  "op": (optional; type int),
  "d": {
    "keys": (optional; type list of strings),
    "values": (optional; list of no set types),
    "texts": (optional; type list of strings)
  },
  "s": (optional; type int),
  "t": (optional; type str)
  }
  ```
# 0.2.2
### Added
- connectionTest() added back
- _Client__gateway_server.runIt(data) #for websocket connections
  - below is a small tutorial on how to use GatewayServer.py to send custom data to Discord:
    - The following initiates a call with a friend and stops the asyncio loop once a message is recieved with event name VOICE_SERVER_UPDATE. Note that you'll need to send a different message to the server to hang up the call.
        ```python
        bot._Client__gateway_server.runIt({
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
        The input for \_Client__gateway_server.runIt is formatted like such:
        ```
        {
          1: {
            "send": [{...}, {...}, {...}],
            "receive": [{...}]
          },
          2: {
            "send": [{...}],
            "receive": [{...}, {...}]
          }
        }
        ```
        tasks are placed in sequencial order (note the 1 and the 2) and are run as such. The 2nd task does not start running until the 1st task has been completed. Each task has "send" and "recieve" sections.      
        The send section denotes what data to send to the server, and it's value is a list of dicts (https://discord.com/developers/docs/topics/gateway). If there are multiple messages to send to the server, each message will be sent before the "receive" section is checked.     
        The receive section (a list of dicts) acts like a search function and each dict is formatted like this: 
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
        An important note about the receive section: if discord sends you multiple messages at once (that is, one after the other without you sending anything), the receive can only check for the last-sent-message. For example, if discord sends a MESSAGE_UPDATE and then a MESSAGE_CREATE, you can only check for the MESSAGE_CREATE.
        As an example, if you'd like to connect to Discord via websockets and never disconnect (until ctrl+c), run the following:
        ```python
        bot._Client__gateway_server.runIt({
          1: {
            "send": [],
            "receive": []
          }
        })
        ```
### Changed
- gateway server protocol greatly simplified. now custom data can be sent to discord via websockets and the websocket connection can be stopped when a certain response is received (based off of https://github.com/Gehock/discord-ws)
- discord's api version updated to api v8, so the self.discord variable updated to https://discord.com/api/v8/

### Removed
- erlang.py

## 0.2.1
### Added
- erlang.py (https://github.com/tenable/DiscordClient/blob/master/erlang.py)
- Login.py to handle logging in (https://github.com/tenable/DiscordClient/blob/master/HttpServer.py)
- Logger.py to print detailed log messages (https://github.com/tenable/DiscordClient/blob/master/Logger.py)
- GatewayServer.py to handle gateway interactions (https://github.com/tenable/DiscordClient/blob/master/GatewayServer.py)
- read session data functions (connects via websockets to Discord) (note: it's recommended that you set update to False because connecting to Discord's gateway server more than 1000 times in 1 day could potentially flag your account):
  - read(update=True)
  - getAnalyticsToken(update=True)
  - getConnectedAccounts(update=True)
  - getConsents(update=True)
  - getExperiments(update=True)
  - getFriendSuggestingCount(update=True)
  - getGuildExperiments(update=True)
  - getGuilds(update=True)
  - getGuildIDs(update=True)
  - getGuildData(guildID,update=True)
  - getGuildOwner(guildID,update=True)
  - getGuildBoostLvl(guildID,update=True)
  - getGuildEmojis(guildID,update=True)
  - getGuildBanner(guildID,update=True)
  - getGuildDiscoverySplash(guildID,update=True)
  - getGuildUserPresences(guildID,update=True)
  - getGuildMsgNotificationSettings(guildID,update=True)
  - getGuildRulesChannelID(guildID,update=True)
  - getGuildVerificationLvl(guildID,update=True)
  - getGuildFeatures(guildID,update=True)
  - getGuildJoinTime(guildID,update=True)
  - getGuildRegion(guildID,update=True)
  - getGuildApplicationID(GuildID,update=True)
  - getGuildAfkChannelID(guildID,update=True)
  - getGuildIcon(guildID,update=True)
  - getGuildName(guildID,update=True)
  - getGuildMaxVideoChannelUsers(guildID,update=True)
  - getGuildRoles(guildID,update=True)
  - getGuildPublicUpdatesChannelID(guildID,update=True)
  - getGuildSystemChannelFlags(guildID,update=True)
  - getGuildMfaLvl(guildID,update=True)
  - getGuildAfkTimeout(guildID,update=True)
  - getGuildHashes(guildID,update=True)
  - getGuildSystemChannelID(guildID,update=True)
  - isGuildLazy(guildID,update=True)
  - getGuildNumBoosts(guildID,update=True)
  - isGuildLarge(guildID,update=True)
  - getGuildExplicitContentFilter(guildID,update=True)
  - getGuildSplashHash(guildID,update=True)
  - getGuildVoiceStates(guildID,update=True)
  - getGuildMemberCount(guildID,update=True)
  - getGuildDescription(guildID,update=True)
  - getGuildVanityUrlCode(guildID,update=True)
  - getGuildPreferredLocale(guildID,update=True)
  - getGuildAllChannels(guildID,update=True)
  - getGuildCategories(guildID,update=True)
  - getGuildCategoryIDs(guildID,update=True)
  - getGuildCategoryData(guildID,categoryID,update=True)
  - getGuildChannels(guildID,update=True)
  - getGuildChannelIDs(guildID,update=True)
  - getGuildChannelData(guildID,channelID,update=True)
  - getGuildMembers(guildID,update=True)
  - getGuildMemberIDs(guildID,update=True)
  - getGuildMemberData(guildID,memberID,update=True)
  - getNotes(update=True)
  - getOnlineFriends(update=True)
  - getDMs(update=True)
  - getDMIDs(update=True)
  - getDMData(DMID,update=True)
  - getDMRecipients(DMID,update=True)
  - getReadStates(update=True)
  - getRelationships(update=True)
  - getRelationshipIDs(update=True)
  - getRelationshipData(RelationshipID,update=True)
  - getFriends(update=True)
  - getFriendIDs(update=True)
  - getBlocked(update=True)
  - getBlockedIDs(update=True)
  - getIncomingFriendRequests(update=True)
  - getIncomingFriendRequestIDs(update=True)
  - getOutgoingFriendRequests(update=True)
  - getOutgoingFriendRequestIDs(update=True)
  - getSessionID(update=True)
  - getTutorial(update=True)
  - getUserData(update=True)
  - getUserGuildSettings(update=True,guildID=None)
  - getUserSettings(update=True)
  - getOptionsForUserSettings(update=True)
  - getWebsocketVersion(update=True)
  - username_to_userID(userdiscriminator)
  - userID_to_username(userID)
- searchMessages(guildID,channelID=None,userID=None,mentionsUserID=None,has=None,beforeDate=None,afterDate=None,textSearch=None,afterNumResults=None)
- filterSearchResults(searchResponse)
- typingAction(channelID)
- deleteMessage(channelID, messageID)
- pinMessage(channelID, messageID)
- unPinMessage(channelID, messageID)
- getPins(channelID)
- snowflake_to_unixts(snowflake)
- unixts_to_snowflake(unixts)
### Changed
- init function now accepts email and password or just token. also proxys are now supported
- the following functions now connect via websockets instead of sending a request to discord's http api:
  -getDMs()
  -getGuilds()
  -getRelationships()

### Removed
- connectionTest function
- Accept-Encoding header

## 0.1.1
### Added
- changeName(name)
- setStatus(status)
- setAvatar(imagePath)
- LoginError exception in case you input incorrect email/password credentials

### Changed
- init now accepts email and password instead of token. this allows for more user functions
- self.discord api url now set in init function. this allows for easily updating the code to match discord's http api version
- sendMessage(channgelID, message, embed="", tts=False) now accepts embedded messages and tts messages
- /messages/embed.py: https://github.com/Merubokkusu/Discord-S.C.U.M/wiki/Messages#send-embed

## 0.1.0
### Added
- sendFile(channelID, filelocation,isurl=False,message="")
- /fileparse/fileparse.py for guessing the type of file based on the file's content (used by sendFile)
- getMessage(channelID,num=1) returns messages in a channel or DM
- getDMs().json() returns a list of DMs
- getGuilds().json() returns a list of guilds
- getRelationships().json() returns a list of relationships (friends, blocked, incoming friend requests, outgoing friend requests)
- requestFriend(userID)
- acceptFriend(userID)
- removeRelationship(userID)
- blockUser(userID)

### Changed
- structure of program: instead of having 1 file with all the commands, various commands are organized into various folders and files
  - all message-related functions are organized in /messages/
  - all file parsing functions are organized in /filetype/
  - all user-related functions are organized in /user/
## 0.0.1
### Added
- easily initiate bot by doing bot = discum.Client(token)
- sendMessage(channelID,message)
- connectionTest() tests if your token is valid

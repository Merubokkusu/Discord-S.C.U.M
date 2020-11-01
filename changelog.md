# Changelog
# 0.2.6
### Added
- ability to turn off logging in bot initiation function (discum.Client())
- ability to toggle logging on/off
- some guild functions (getInfoFromInviteCode, joinGuild, kick, ban, getGuildMember)
- a message function (createDM)
- \_Client__gateway_server.run(data,log) now returns the targeted responses in a list
### Changed
- discum.Client now has a logging option:
  ```python
  discum.Client(email="none", password="none", token="none", proxy_host=False, proxy_port=False, user_agent="random", log=True)
  ```
- \_Client__gateway_server.runIt(data,log) is now bot.\_Client__gateway_server.run(data,log)
- \_Client__gateway_server.run requires the log input (True or False)
- updated gateway protocol to process current session settings format
- simplified discum.py by removing 1 useless class (that turned str(dictionaries) into classes) and 1 useless function (that turned dictionaries into strings)
- ```bot.getGuildMembers(guildID,update=True)``` --> ```bot.getGuildCachedMembers(guildID,update=True)```
- ```bot.getGuildMemberIDs(guildID,update=True)``` --> ```bot.getGuildCachedMemberIDs(guildID,update=True)```
- ```bot.getGuildMemberData(guildID,memberID,update=True)``` --> ```bot.getGuildCachedMemberData(guildID,memberID,update=True)```
### Removed
The following functions were removed in this version due to discord changing its session settings format (gateway server). These functions (or many of them) will be added in the next version as http api requests:  
```bot.getGuildData(guildID,update=True)```     
```bot.getGuildOwner(guildID,update=True)```     
```bot.getGuildBoostLvl(guildID,update=True)```     
```bot.getGuildEmojis(guildID,update=True)```     
```bot.getGuildBanner(guildID,update=True)```     
```bot.getGuildDiscoverySplash(guildID,update=True)```     
```bot.getGuildUserPresences(guildID,update=True)```     
```bot.getGuildMsgNotificationSettings(guildID,update=True)```     
```bot.getGuildRulesChannelID(guildID,update=True)```     
```bot.getGuildVerificationLvl(guildID,update=True)```     
```bot.getGuildFeatures(guildID,update=True)```     
```bot.getGuildJoinTime(guildID,update=True)```     
```bot.getGuildRegion(guildID,update=True)```     
```bot.getGuildApplicationID(GuildID,update=True)```     
```bot.getGuildAfkChannelID(guildID,update=True)```     
```bot.getGuildIcon(guildID,update=True)```     
```bot.getGuildName(guildID,update=True)```     
```bot.getGuildMaxVideoChannelUsers(guildID,update=True)```     
```bot.getGuildRoles(guildID,update=True)```     
```bot.getGuildPublicUpdatesChannelID(guildID,update=True)```     
```bot.getGuildSystemChannelFlags(guildID,update=True)```     
```bot.getGuildMfaLvl(guildID,update=True)```     
```bot.getGuildAfkTimeout(guildID,update=True)```     
```bot.getGuildHashes(guildID,update=True)```     
```bot.getGuildSystemChannelID(guildID,update=True)```     
```bot.isGuildLazy(guildID,update=True)```     
```bot.getGuildNumBoosts(guildID,update=True)```     
```bot.isGuildLarge(guildID,update=True)```     
```bot.getGuildExplicitContentFilter(guildID,update=True)```     
```bot.getGuildSplashHash(guildID,update=True)```   
```bot.getGuildMemberCount(guildID,update=True)```     
```bot.getGuildDescription(guildID,update=True)```     
```bot.getGuildVanityUrlCode(guildID,update=True)```     
```bot.getGuildPreferredLocale(guildID,update=True)```     
```bot.getGuildAllChannels(guildID,update=True)```     
```bot.getGuildCategories(guildID,update=True)```     
```bot.getGuildCategoryIDs(guildID,update=True)```     
```bot.getGuildCategoryData(guildID,categoryID,update=True)```     
```bot.getGuildChannels(guildID,update=True)```     
```bot.getGuildChannelIDs(guildID,update=True)```     
```bot.getGuildChannelData(guildID,channelID,update=True)```     
# 0.2.5
### Added
- ability to set custom user agent (or randomly generate a user agent). This user agent is then used for both http api requests and websocket connections
- colorful GatewayServer outputs
### Changed
- discum.Client input:
  ```python
  bot = discum.Client(email='', password='', token='', proxy_host=None, proxy_port=None, user_agent="random")
  ```
- gateway version from v6 to v8
- task receive checking, again. made it a lot simpler and better. See following example for getting members of a server with a little under 200 members:
  ```python
  bot._Client__gateway_server.runIt({
    1: {
      "send": [{
        "op": 14,
        "d": {
          "guild_id": GUILD_ID,
          "channels": {
            TEXT_CHANNEL_ID: [
              [0, 99],
              [100, 199]
            ]
          }
        }
      }],
      "receive": [{
        "key": [('d', 'ops', 0, 'range'), ('d', 'ops', 1, 'range')],
        "keyvalue": [(('d', 'ops', 0, 'op'), 'SYNC'), (('d', 'ops', 1, 'op'), 'SYNC')]
      }]
    }
  })
  ```
  the receive format is greatly simplified :)
  ```
  {
  "key":(optional; type list of tuples of strings/ints),
  "keyvalue": (optional; type list of tuples of key&value)
  }
  ```
  this might be more helpful: how to use the receive format:
  ```
  {
  "key": [("keys","in","nesting","order"),("keys2","in2","nesting2","order2"),...]
  "keyvalue": [(("keys","in","nesting","order"),value_to_check_for2),(("keys2","in2","nesting2","order2"),value_to_check_for2),...]
  }
  ```
  and to clear up any confusion, key looks for the existence of keys and keyvalue looks to see if a specific key has a specific value. Since you can check multiple keys and/or multiple key-value pairs per task, the possibilities are literally endless for what you can look for :)
# 0.2.4
### Changed
- task receive checking (in gateway/GatewayServer.py) for better searching thru nested dictionaries. see the following example for getting the members of a server that has a little over 300 members:
  ```python
  bot._Client__gateway_server.runIt({
    1: {
      "send": [{
        "op": 14,
        "d": {
          "guild_id": GUILD_ID,
          "channels": {
            TEXT_CHANNEL_ID: [
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
          "guild_id": GUILD_ID,
          "channels": {
            TEXT_CHANNEL_ID: [
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
  "keyvaluechecker": [["list","of","keys","in","the","order","which","they","are","nested","in"],value_to_check_for]
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

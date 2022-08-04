# Changelog
# 1.4.1
### Added
- getChannel, getGuildActivitiesConfig, and getMutualFriends rest api wraps
- getGuildRoles (https://github.com/Merubokkusu/Discord-S.C.U.M/commit/faa75c3234cdf89e0f93873d612aecd84262e5c1)
### Changed
- updated searchMessages to work on both guilds and dms
- x-debug-options bugReporterEnabled header
- updated validatePhone (ty sheepsushis)
- slash commands (ty vivinano) and buttons
- documentation edits (ty SCR33M)
- gateway updates (https://github.com/Merubokkusu/Discord-S.C.U.M/commit/ccec86e9c46cac22f0e5f925348fe322e1a8760a, https://github.com/Merubokkusu/Discord-S.C.U.M/commit/16b00f36fb0cd4357d36af8122a2ff6555c368f3)
- fix printing + interactions (ty BalaM314, BadozChopra, and dolfies)
- updated user agent default and build number fetching (https://github.com/Merubokkusu/Discord-S.C.U.M/commit/a814f9500429ebd6b31c93cbae3c330bd8f1f89a)
- creating guilds with templates (https://github.com/Merubokkusu/Discord-S.C.U.M/commit/8844620c59685c72cdd229b383dd79a995a6ab6b)
- fixed incorrect padding issue in login.py
# 1.4.0
### Added
- getRelationships, getVoiceRegions, getHandoffToken
- suppressEveryonePings, suppressRoleMentions, enableMobilePushNotifications, setChannelNotificationOverrides, setMessageNotifications, muteGuild, muteDM
- getRoleMemberCounts, getGuildIntegrations, getGuildTemplates, getRoleMemberIDs, addMembersToRole, setMemberRoles
- createGuild, deleteGuild, previewGuild, getDiscoverableGuilds, deleteChannel, getGuildInvites, getChannelInvites, getGuildRegions, getGuildChannels
- __DM groups__: removeFromDmGroup, addToDmGroup, createDmGroupInvite, setDMGroupName, setDmGroupIcon, deleteInvite
- setPhone and validatePhone (thx sudo-do)
- __Threads__: setThreadNotifications, createThread, leaveThread, joinThread, archiveThread, unarchiveThread
- __School hubs__: lookupSchool, schoolHubSignup, schoolHubWaitlistSignup, schoolHubSignup, verifySchoolHubSignup, getSchoolHubGuilds, getSchoolHubDirectoryCounts, joinGuildFromSchoolHub, searchSchoolHub, getMySchoolHubGuilds, setSchoolHubGuildDetails
- getLiveStages
- setProfileColor
- __Interactions__: getSlashCommands (only if you share a dm with the bot), triggerSlashCommand, click
- getReportMenu, reportSpam
- setUserNote
- inviteToCall, declineCall
- utils.slash.SlashCommander (from discum.utils.slash import SlashCommander) to craft slash command interaction data
- utils.button.Buttoner (from discum.utils.button import Buttoner) to craft button/dropdown interaction data
- gateway.request.searchSlashCommands (only for guilds), gateway.queryGuildMembers (op8 "brute forcing" now possible), and gateway.checkGuildMembers 
- remote auth functions (initRA, remoteAuthLogin) + ability to add/remove functions to the remote auth gateway (ra)
- 4 functions to gateway.session.guild(guildID): applicationCommandCount, maxMembers, stages, and stickers
- gateway.connectionKwargs variable (dict): possible key values = "proxy\_type", "http\_proxy\_auth"; see issue #153
### Changed
- use \_\_slots__ to lower ram usage
- only import stuff when needed (speed up imports)
- fixed login (thx MayaankAshok)
- fixed color printing for windows
- renamed gateway.session.guild(guildID).position to gateway.session.guild(guildID).me
- updated ready event parsing to use the value of "users" to provide full user data to DM recipients and relationships (thx dolfies)
### Removed
- getGuildMember

# 1.3.1
### Added
- checkPermissions function to permissions.py
- gateway event type parsing for messages, channels, and relationships
- organized some files that were being used in multiple contexts into utils folder
- search guild members (opcode 8) examples
- more searchMessages queries
- accessibility.py to calculate and parse the accessibility number (sent in discord's "science"/tracking requests)
- color.py to help with getting color values
- 4 resp api wraps: greet, setAboutMe, setBanner, and getGuilds
- findVisibleChannels (looks for channels and categories)
- thread\_member\_lists argument added to op14 request wrap
- contextproperties.py to add the X-Context-Properties header to some requests
### Changed
- typo in http request headers fixed (thx dolfies)
- capabilities # in gateway identify msg updated
- updated embed examples (thx caiocinel)
- subscribeToGuildEvents also works for unavailable guilds
- updated message parsing
# 1.3.0
### Added
- more message types to discum/gateway/messages/parse.py
- gateway close code handlers
- gateway latency calculation (bot.gateway.latency)
- permissions code to the guild REST api wrap folder
- finished user settings REST api wraps
### Changed
- removed timeout parameter from status update commands. setPlayingStatus, setStreamingStatus, setListeningStatus, and setWatchingStatus do not work currently. Will be fixed in the future if a fix is found.
- use try-catch to find correct import instead of sys
- fixed gateway heartbeat sequence
- REST api response now prints even if a 401 status code is received
- checkConnection() replaced with checkToken(token)
- rewrote the docs
# 1.2.1
### Added
- channel\_create and channel\_delete parser methods
- channel\_create and channel\_delete gateway.session updates
- multibots example
### Changed
- gateway.run(auto_reconnect=True) now only disconnects on gateway.close() and ctrl-c
- fetch members now checks how many members have been fetched instead of how many members were requested for (important for knowing when to stop fetching members for small guilds)
- organized RESTapiwrap.py
- updated api version to v9
- updated superproperties creation to include system-locale key only if token is not used for bot initialization

# 1.2.0
### Added
- added guild_create parsing function
- added sessions_replace parsing function (to better sync the client and discord when updating activities)
- added parsing functions for ready and ready_supplemental
- added guild_members_chunk event parsing
- added headerModification ability to RESTapiwrap (because some api wraps do not require the authorization header)
- added ability to speed up client initialization by setting the build number (this is useful for running multiple bots):
    ```python
    bot = discum.Client(token=tokenlist[0])
    build_num = bot._Client__super_properties['client_build_number']
    clients = [bot]
    for token in tokenlist[1:]:
        clients.append(discum.Client(token=token, build_num=build_num))
    ```
- added ability to set and remove statuses and activities (gateway functions):
    ```python
    bot.gateway.setStatus(status)
    bot.gateway.setCustomStatus(customstatus, emoji=None, animatedEmoji=False, expires_at=None)
    bot.gateway.removeCustomStatus()
    bot.gateway.setPlayingStatus(game)
    bot.gateway.removePlayingStatus()
    bot.gateway.setStreamingStatus(stream, url)
    bot.gateway.removeStreamingStatus()
    bot.gateway.setListeningStatus(song)
    bot.gateway.removeListeningStatus()
    bot.gateway.setWatchingStatus(show)
    bot.gateway.removeWatchingStatus()
    bot.gateway.clearActivities()
    ```
### Changed
- reformatted session data
  - ready event:
    - merged_members field used to predict current role in guild
    - relationships is a dict instead of a list
    - private_channels (DMs) is a dict instead of a list
    - guilds is a dict instead of a list
    - within guilds: emojis, roles, and channels are dicts instead of lists
  - ready_supplemental event:
    - online_friends is a dict instead of a list
    - voice_states is a dict instead of a list
- moved setting status commands to gateway
- cleaned searchMessages http function
### Removed
- all "merged" functions from /discum/gateway/session.py
# 1.1.0
### Added
- 3 http api wraps: leaveGuild, createInvite, revokeBan
- stopIndex param to fetchMembers (making guild member requesting behavior/style now completely controllable)
### Changed
- fixed fetchMember's wait param (now waits a specified number of seconds after previous response)
- modified http api request headers to better mimic web client
- added brotli decompression support (other decompression types handled automatically by requests module)
- gateway heartbeat now occurs exactly after that many milliseconds specified by HELLO response (used to occur 2 seconds less)
- discum.Client(...) now accepts locale as a parameter

# 1.0.1
### Added
- more 56 http api wraps:
  ```python
  bot.login(email, password, undelete=False, captcha=None, source=None, gift_code_sku_id=None, secret="", code="")
  bot.getXFingerprint()
  bot.getBuildNumber()
  bot.getSuperProperties(user_agent, buildnum="request")
  bot.getGatewayUrl()
  bot.getDiscordStatus()
  bot.getDetectables()
  bot.getOauth2Tokens()
  bot.getVersionStableHash(underscore=None)
  bot.bulkAck(data)
  bot.getTrendingGifs(provider="tenor", locale="en-US", media_format="mp4")
  bot.getStickers(directoryID="758482250722574376", store_listings=False, locale="en-US")
  bot.getStickerFile(stickerID, stickerAsset)
  bot.getStickerJson(stickerID, stickerAsset)
  bot.getStickerPack(stickerPackID)
  bot.setUsername(username)
  bot.setEmail(email)
  bot.setPassword(new_password)
  bot.setDiscriminator(discriminator)
  bot.getProfile(userID)
  bot.info(with_analytics_token=None)
  bot.getUserAffinities()
  bot.getGuildAffinities()
  bot.getMentions(limit=25, roleMentions=True, everyoneMentions=True)
  bot.removeMentionFromInbox(messageID)
  bot.setHypesquad(house)
  bot.leaveHypesquad()
  bot.setLocale(locale)
  bot.calculateTOTPcode(secret="default")
  bot.getTOTPurl(secret): #use this to store your totp secret/qr pic; btw url format is otpauth://totp/Discord
  bot.enable2FA()
  bot.disable2FA(code="calculate", clearSecretAfter=False)
  bot.getRTCregions()
  bot.setAFKtimeout(timeout_seconds)
  bot.setTheme(theme)
  bot.setMessageDisplay(CozyOrCompact)
  bot.enableDevMode(enable)
  bot.activateApplicationTestMode(applicationID)
  bot.getApplicationData(applicationID, with_guild=False)
  bot.getBackupCodes(regenerate=False)
  bot.enableInlineMedia(enable)
  bot.enableLargeImagePreview(enable)
  bot.enableGifAutoPlay(enable)
  bot.enableLinkPreview(enable)
  bot.enableReactionRendering(enable)
  bot.enableAnimatedEmoji(enable)
  bot.enableEmoticonConversion(enable)
  bot.setStickerAnimation(setting)
  bot.enableTTS(enable)
  bot.getBillingHistory(limit=20)
  bot.getPaymentSources()
  bot.getBillingSubscriptions()
  bot.getStripeClientSecret()
  bot.logout(provider=None, voip_provider=None)
  bot.getMemberVerificationData(guildID, with_guild=False, invite_code=None)
  bot.agreeGuildRules(guildID, form_fields, version="2021-01-31T02:41:24.540000+00:00")
  ```
- ability to login to accounts that have 2FA (either input code or secret) (no sms login support yet, however)
- ability to send science requests (along with automatic (sequencial) client uuid calculation, client_send_timestamp, and client_track_timestamp if not inputted)
- ability to parse client uuids (and have a good guess of when the client uuid was calculated and for which user id)
- function to reply to messages (bot.reply(...))
- Embedder object initialization on client start
### Changed
- bot.setStatus accepts "online"/"idle"/"dnd"/"invisible" as inputs instead of 0/1/2/3
- bot.sendMessage and bot.sendFile to allow for replies and stickers
# 1.0.0
### Added
- gateway functions/wraps structure
- added documentation for extending and reading discum
- inline field to embed
- ability to fetch guild members (gateway.fetchMembers(...) function) ([example](https://github.com/Merubokkusu/Discord-S.C.U.M/blob/master/examples/gettingGuildMembers.py))
- gateway.finishedMemberFetching() function
- some gateway.session functions to access and modify member dictionary
- response.py, event.py, parse.py, and request.py
- event checking
- response parsing (and auto-parsing)
### Changed
- resp is now an Resp object with 3 attributes ([example](https://github.com/Merubokkusu/Discord-S.C.U.M/blob/master/examples/respexample.py)):
  - raw (just the decompressed dictionary response)
  - event (allows for resp.event... event checking)
  - parsed (allows for resp.parsed... parsing)
- organized documentation on using discum
# 0.3.1
### Added
- gateway decompression (zlib-stream)
- super-properties to http headers
- ability to get xfingerprint (used for login if only username and password are given, see login.py)
### Changed
- proxy inputs/parsing
- search-messages function
- organized client initialization
# 0.3.0
### Added
- gateway interactions rewritten to use websocket.WebSocketApp from https://github.com/websocket-client/websocket-client
- ability to have functions run on every receive message (influenced by this: https://github.com/scrubjay55/Reddit_ChatBot_Python/blob/master/Reddit_ChatBot_Python/Utils/WebSockClient.py)
for example:
   ```python
   @bot.gateway.command
   def helloworld(resp):
       if resp['t'] == "READY_SUPPLEMENTAL": #ready_supplemental is sent after ready
           user = bot.gateway.SessionSettings.user
           print("Logged in as {}#{}".format(user['username'], user['discriminator']))
       if resp['t'] == "MESSAGE_CREATE":
           m = resp['d']
           guildID = m['guild_id'] if 'guild_id' in m else None #because DMs are technically channels too
           channelID = m['channel_id']
           username = m['author']['username']
           discriminator = m['author']['discriminator']
           content = m['content']
           print("> guild {} channel {} | {}#{}: {}".format(guildID, channelID, username, discriminator, content))
   
   bot.gateway.run(auto_reconnect=True)
   ```
- ability to reconnect and properly send resume messages to discord when possible
- check for and properly handle SESSION_INVALID events
- added support for python 2.7
### Changed
- simplified gateway code
- simplified gateway api
- reorganized session settings
### Removed
- old gateway interaction code (replaced with better code)

# 0.2.8
### Added
```python
addReaction(channelID,messageID,emoji)
removeReaction(channelID,messageID,emoji)
ackMessage(channelID,messageID,ackToken=None)
unAckMessage(channelID,messageID,numMentions=0)
```
ability to limit task duration (in seconds) and ability to collect certain responses:
for example, the following collects MESSAGE_CREATE and MESSAGE_UPDATE messages for 10 seconds:
```python
>>> bot._Client__gateway_server.run(
    [
        {
            "send": [],
            "receive": [],
            "collect": [
                {
                    "keyvalue": [
                        (
                            ("t",),
                            "MESSAGE_CREATE",
                        )
                    ],
                },
                {
                    "keyvalue": [
                        (
                            ("t",),
                            "MESSAGE_UPDATE",
                        )
                    ],
                }
            ],
            "limit": 10,
        }
    ],
    log=False,
)
>>> latest_messages = bot._Client__gateway_server.collected #collected messages
>>> len(latest_messages) #only 1 task was inputted, so output is 1
1
>>> for item in latest_messages[0]:
...    print(item['t'])
...
MESSAGE_CREATE
MESSAGE_UPDATE
MESSAGE_CREATE
MESSAGE_UPDATE
```
### Changed
- gateway server input is now a list of lists (1st list is the first task, 2nd list is the 2nd task, etc)

# 0.2.7
### Added
- added these functions back as websockets (since the web client doesn't use the http api to fetch guild data):
```python
getGuildIDs(update=True)
getGuildData(guildID,update=True)
getGuildOwner(guildID,update=True)
getGuildBoostLvl(guildID,update=True)
getGuildEmojis(guildID,update=True)
getGuildBanner(guildID,update=True)
getGuildDiscoverySplash(guildID,update=True)
getGuildMsgNotificationSettings(guildID,update=True)
getGuildRulesChannelID(guildID,update=True)
getGuildVerificationLvl(guildID,update=True)
getGuildFeatures(guildID,update=True)
getGuildJoinTime(guildID,update=True)
getGuildRegion(guildID,update=True)
getGuildApplicationID(guildID,update=True)
getGuildAfkChannelID(guildID,update=True)
getGuildIcon(guildID,update=True)
getGuildName(guildID,update=True)
getGuildMaxVideoChannelUsers(guildID,update=True)
getGuildRoles(guildID,update=True)
getGuildPublicUpdatesChannelID(guildID,update=True)
getGuildSystemChannelFlags(guildID,update=True)
getGuildMfaLvl(guildID,update=True)
getGuildAfkTimeout(guildID,update=True)
getGuildHashes(guildID,update=True)
getGuildSystemChannelID(guildID,update=True)
isGuildLazy(guildID,update=True)
getGuildNumBoosts(guildID,update=True)
isGuildLarge(guildID,update=True)
getGuildExplicitContentFilter(guildID,update=True)
getGuildSplashHash(guildID,update=True)
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
getGuildVoiceStates(guildID,update=True)
getGuildNotOfflineCachedMembers(guildID,update=True)
getGuildNotOfflineCachedMemberIDs(guildID,update=True)
getGuildNotOfflineCachedMemberData(guildID,userID,update=True)
getMergedPresences(update=True)
getAllGuildsMergedPresences(update=True)
getGuildMergedPresences(guildID,update=True)
getGuildMergedPresencesIDs(update=True)
getGuildMergedPresencesData(guildID,userID,update=True)
getAllFriendsMergedPresences(update=True)
getAllFriendsMergedPresencesIDs(update=True)
getFriendMergedPresencesData(userID,update=True)
getAllMyGuildPositions(update=True)
getMyGuildPosition(guildID,update=True)
```
### Changed
- fixed session settings processing (session settings started getting sent in 2 parts: READY and READY_SUPPLEMENTAL)
- changed timing in GatewayServer.py to better mimic the web client (start processing tasks after READY_SUPPLEMENTAL is received)

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
The following functions were removed in this version due to discord changing its session settings format (gateway server). These functions (or many of them) will be added in the next version as ~~http api requests~~ (figured out how to do it with websockets again; deciding against http api for this since official discord clients use websockets for the tasks below):  
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

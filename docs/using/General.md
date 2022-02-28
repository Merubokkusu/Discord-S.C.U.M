# Some info on variables and data
- [Variables](#Variables)
    - [logging](#logging)
    - [general variables](#general-variables)
    - [gateway variables](#gateway-variables)
        - [session data/settings](#botgatewaysession)
        
- [Functions](#Functions)
    - [check token](#checkToken)
    - [switch account](#switchAccount)
    - [switch proxy](#switchProxy)
    - [convert between snowflake and unixts](#snowflake_to_unixts-and-unixts_to_snowflake)
    - [gateway functions](#gateway-functions)
        - [add functions to gateway command list](#gatewaycommand)
        - [remove functions from gateway command list](#gatewayremoveCommand)
        - [clear gateway command list](#gatewayclearCommands)
        - [reset gateway session](#gatewayresetSession)
        - [send payload to gateway](#gatewaysend)
        - [auto parse gateway responses](#respparsedauto)
        - [event checking](events.md)

## Variables

### logging
```bot.log``` dict, manages logging for REST actions. "encoding" is optional and defaults to 'utf-8'.
```python
bot.log = {"console":True, "file":False}
#or
bot.log = {"console":False, "file":"log.txt", "encoding":"utf-8"}
#etc...
```
```bot.gateway.log``` dict, manages logging for gateway actions (live events, websocket)
```python
bot.gateway.log = {"console":True, "file":False}
#or
bot.gateway.log = {"console":False, "file":"gatewaylog.txt", "encoding":"utf-8"}
#etc...
```
```bot.ra.log``` dict, manages logging for remote authentication gateway actions (login thru qr-code)
```python
bot.ra.log = {"console":True, "file":False}
#or
bot.ra.log = {"console":False, "file":"ralog.txt", "encoding":"utf-8"}
#etc...
```

### general variables
```python
bot._Client__user_token
bot._Client__user_email
bot._Client__user_password
bot._Client__totp_secret
bot._Client__xfingerprint
bot._Client__user_agent
bot._Client__super_properties
bot.api_version
bot.discord #REST api base url
bot.websocketurl
bot.s #requests.Session object
bot.gateway #GatewayServer object
bot.Science #placeholder variable for science events
```

### gateway variables
```bot.gateway.keepData```   default value is ("dms", "guilds", "guild_channels"), which means that data from these are kept in session data even after being kicked/banned from or removing them. This is to prevent accidental data deletion. You can use the removeDmData, removeGuildData, removeChannelData [session functions](#botgatewaysession) to remove these from memory.

```python
bot.gateway.auth #data for IDENTIFY msg
bot.gateway.RESTurl #in case this is needed
bot.gateway.sessionobj #same as bot.s, just in case this is needed
```

```python
bot.gateway._after_message_hooks #where all the gateway commands are added
```

```python
bot.gateway.interval #received from discord
bot.gateway.session_id #received from discord
bot.gateway.sequence #msg counter for heartbeating
bot.gateway.READY #becomes True once READY_SUPPLEMENTAL is received
bot.gateway.connected #boolean
bot.gateway.resumable #boolean
bot.gateway._last_ack #when last HEARTBEAT_ACK was received
bot.gateway.latency #seconds between HEARTBEAT and HEARTBEAT_ACK
bot.gateway._last_err #last detected error
bot.gateway._last_close_event #last close event
```

```python
bot.gateway.proxy_host
bot.gateway.proxy_port
bot.gateway.proxy_type
bot.gateway.proxy_auth
```

```python
bot.gateway.memberFetchingStatus #used by fetchMembers and finishedMemberFetching to keep track of member fetching status
bot.gateway.resetMembersOnSessionReconnect #some member fetching processes take longer than a session. To prevent member data from the previous session from being wiped, set this to True.
bot.gateway.updateSessionData #set to False to stop session data from updating. This can break certain gateway actions that require session data.
bot.gateway.guildMemberSearches #where queries and userIDs from opcode 8 searches are stored
```
```python
bot.gateway.request #gateway request object
```

#### bot.gateway.session
(Session Data/Settings)
##### Your session settings are tied to your last gateway connection.

All of the session data:

``` python
bot.gateway.session.read()
```

Save some memory by deleting essentially useless data (some user data from ready and ready supplemental):

``` python
bot.gateway.session.saveMemory()
```

General data:

``` python
bot.gateway.session.user
bot.gateway.session.guilds
bot.gateway.session.allGuildIDs
bot.gateway.session.guildIDs
bot.gateway.session.setGuildData(guildID, guildData)
bot.gateway.session.removeGuildData(guildID)
bot.gateway.session.setDmData(channelID, channelData)
bot.gateway.session.removeDmData(channelID)
bot.gateway.session.setVoiceStateData(guildID, voiceStateData)
bot.gateway.session.relationships
bot.gateway.session.relationshipIDs
bot.gateway.session.friends
bot.gateway.session.friendIDs
bot.gateway.session.blocked
bot.gateway.session.blockedIDs
bot.gateway.session.incomingFriendRequests
bot.gateway.session.incomingFriendRequestIDs
bot.gateway.session.outgoingFriendRequests
bot.gateway.session.outgoingFriendRequestIDs
bot.gateway.session.onlineFriends
bot.gateway.session.onlineFriendIDs
bot.gateway.session.DMs
bot.gateway.session.DMIDs
bot.gateway.session.userGuildSettings
bot.gateway.session.userSettings
bot.gateway.session.optionsForUserSettings
bot.gateway.session.updateUserSettings(data)
bot.gateway.session.analyticsToken
bot.gateway.session.connectedAccounts
bot.gateway.session.consents
bot.gateway.session.experiments
bot.gateway.session.friendSuggestionCount
bot.gateway.session.guildExperiments
bot.gateway.session.readStates
bot.gateway.session.geoOrderedRtcRegions
bot.gateway.session.cachedUsers
bot.gateway.session.tutorial
```

Data and functions about a specific guild:

``` python
bot.gateway.session.guild(guildID).data
bot.gateway.session.guild(guildID).setData(newData)
bot.gateway.session.guild(guildID).updateData(data)
bot.gateway.session.guild(guildID).unavailable
bot.gateway.session.guild(guildID).hasMembers
bot.gateway.session.guild(guildID).members
bot.gateway.session.guild(guildID).memberIDs
bot.gateway.session.guild(guildID).resetMembers()
bot.gateway.session.guild(guildID).updateOneMember(userID, userProperties)
bot.gateway.session.guild(guildID).updateMembers(memberdata)
bot.gateway.session.guild(guildID).owner
bot.gateway.session.guild(guildID).boostLvl
bot.gateway.session.guild(guildID).emojis
bot.gateway.session.guild(guildID).emojiIDs
bot.gateway.session.guild(guildID).banner
bot.gateway.session.guild(guildID).discoverySplash
bot.gateway.session.guild(guildID).msgNotificationSettings
bot.gateway.session.guild(guildID).rulesChannelID
bot.gateway.session.guild(guildID).verificationLvl
bot.gateway.session.guild(guildID).features
bot.gateway.session.guild(guildID).joinTime
bot.gateway.session.guild(guildID).region
bot.gateway.session.guild(guildID).applicationID
bot.gateway.session.guild(guildID).afkChannelID
bot.gateway.session.guild(guildID).icon
bot.gateway.session.guild(guildID).name
bot.gateway.session.guild(guildID).maxVideoChannelUsers
bot.gateway.session.guild(guildID).roles
bot.gateway.session.guild(guildID).publicUpdatesChannelID
bot.gateway.session.guild(guildID).systemChannelFlags
bot.gateway.session.guild(guildID).mfaLvl
bot.gateway.session.guild(guildID).afkTimeout
bot.gateway.session.guild(guildID).hashes
bot.gateway.session.guild(guildID).systemChannelID
bot.gateway.session.guild(guildID).lazy
bot.gateway.session.guild(guildID).numBoosts
bot.gateway.session.guild(guildID).large
bot.gateway.session.guild(guildID).threads
bot.gateway.session.guild(guildID).explicitContentFilter
bot.gateway.session.guild(guildID).splashHash
bot.gateway.session.guild(guildID).memberCount
bot.gateway.session.guild(guildID).description
bot.gateway.session.guild(guildID).vanityUrlCode
bot.gateway.session.guild(guildID).preferredLocale
bot.gateway.session.guild(guildID).updateChannelData(channelID, channelData)
bot.gateway.session.guild(guildID).setChannelData(channelID, channelData)
bot.gateway.session.guild(guildID).removeChannelData(channelID)
bot.gateway.session.guild(guildID).channelsAndCategories
bot.gateway.session.guild(guildID).allChannelAndCategoryIDs
bot.gateway.session.guild(guildID).channelAndCategoryIDs
bot.gateway.session.guild(guildID).categories
bot.gateway.session.guild(guildID).categoryIDs
bot.gateway.session.guild(guildID).category(categoryID)
bot.gateway.session.guild(guildID).channels
bot.gateway.session.guild(guildID).channelIDs
bot.gateway.session.guild(guildID).channel(channelID)
bot.gateway.session.guild(guildID).voiceStates
bot.gateway.session.guild(guildID).me
bot.gateway.session.guild(guildID).applicationCommandCount
bot.gateway.session.guild(guildID).maxMembers
bot.gateway.session.guild(guildID).stages
bot.gateway.session.guild(guildID).stickers
```

Data about a specific relationship:

``` python
bot.gateway.session.relationship(userID).data
```

Data and functions about a specific DM:

``` python
bot.gateway.session.DM(DMID).data
bot.gateway.session.DM(DMID).updateData(data)
bot.gateway.session.DM(DMID).recipients
```

User settings data about a specific guild (like notifications, etc):

``` python
bot.gateway.session.userGuildSetting(guildID).data
```

## Functions
##### ```checkToken```
```python
bot.checkToken('poop')
```
###### Parameters:
- token (str)
###### Returns:
a requests.Response object. If the token is valid, the .json() should contain the following keys:        
\['id', 'username', 'avatar', 'discriminator', 'public_flags', 'flags', 'locale', 'nsfw_allowed', 'mfa_enabled', 'analytics_token', 'email', 'verified', 'phone'\]

##### ```switchProxy```
```python
bot.switchProxy('http://username:password123@127.0.0.1:8080')
#do stuff
bot.switchProxy('https://192.168.1.18:4444')
#do other stuff
```
###### Parameters:
- newProxy (str/None) - set to None to not use a proxy
	examples:       
		"http://10.10.1.10:3128"       
		"http://username:password123@10.10.1.10:3128"       
		"https://10.10.1.10:3126"       
		"socks4://10.10.1.10:3126"
- updateGateway (Optional[bool]) - update proxy for gateway. Defaults to True

##### ```switchAccount```
```python
bot.switchAccount('token')
```
###### Parameters:
- newToken (str)

##### ```snowflake_to_unixts``` and ```unixts_to_snowflake```
```python
bot.snowflake_to_unixts("842574767584182273")
bot.unixts_to_snowflake("1620955878.87425")
```
###### Parameters:
- snowflake or unixts (depending on which conversion you're using) (str/int/float)

###### Returns:
bot.snowflake_to_unixts -> float        
bot.unixts_to_snowflake -> int        

### gateway functions

##### ```gateway.command```
adding a function **without** extra parameters to the gateway command list:
```python
@bot.gateway.command
def myfunction(resp):
    pass
```
or
```python
def myfunction(resp):
    pass

bot.gateway.command(function)
```
or adding a function **with** extra parameters to the gateway command list:
```python
def myfunction(resp, guild_id, channel_id, log=True):
    if log: print(guild_id, channel_id)

bot.gateway.command(
    {
        "function": myfunction,
        "priority": 0,
        "params": {"guild_id": "123123123", "channel_id": "321321321", "log": True},
    }
)
```
###### Parameters:
- function (function/dict) - function if no extra params needed, dict if extra params needed.       
  Dict version also allows you to specify a priority (optional) where 0 indicates top priority and -1 indicates lowest priority. Think of priority as a command   list index.

##### ```gateway.removeCommand```
```python
bot.gateway.removeCommand(myfunction)
```
###### Parameters:
- function (function/dict) - the function you want to remove
- exactMatch (bool) - only useful if a dict is passed as the function. Will only look for exact dictionary matches if set to True. Else, it will just look for function matches. Defaults to True
- allMatches (bool) - if set to False, only the first match will be removed. Defaults to False

##### ```gateway.clearCommands```
```python
bot.gateway.clearCommands()
```
##### ```gateway.run```
```python
bot.gateway.run()
```
###### Parameters:
- auto_reconnect (bool) - auto reconnect (resume when possible) for all cases except bot.gateway.close() and ctrl-c. Defaults to True

##### ```gateway.close```
```python
@bot.gateway.command
def test(resp):
    bot.gateway.close()
```
##### ```gateway.resetSession```
Do not run this while connected to the gateway. Only run this after you've closed the gateway connection.
```python
bot.gateway.resetSession()
```
##### ```gateway.send```
```python
@bot.gateway.command
def test(resp):
    if resp.event.ready_supplemental:
        bot.gateway.send({"op": 1,"d": 0})
```
###### Parameters:
- payload (dict) - what to send to the gateway

##### ```resp.parsed.auto```
```python
@bot.gateway.command
def test(resp):
    if resp.event.message:
        m = resp.parsed.auto()
        print(m['type'])
```

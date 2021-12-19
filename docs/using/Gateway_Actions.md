# Gateway Actions
the request functions do not return anything      
the parse functions return dictionaries       
_____________
### Start
##### ```resp.parsed.ready```
```python
@bot.gateway.command
def readyTest(resp):
    if resp.event.ready:
        print("received ready event")
```
##### ```resp.parsed.ready_supplemental```
used for checking if we've successfully connected to the gateway
```python
@bot.gateway.command
def readySuppTest(resp):
    if resp.event.ready_supplemental:
        print("received ready supplemental event")
```
_____________
### User
##### ```gateway.setStatus```
```python
@bot.gateway.command
def setStatusTest(resp):
    if resp.event.ready_supplemental:
        bot.gateway.setStatus("online")
```
###### Parameters:
- status (str) - "online", "idle", "dnd", or "invisible"

##### ```gateway.setCustomStatus```
```python
@bot.gateway.command
def setStatusTest(resp):
    if resp.event.ready_supplemental:
        bot.gateway.setCustomStatus("Discording")
```
###### Parameters:
- customstatus (str)
- emoji (Optional[str])
- animatedEmoji (Optional[bool]) - is the emoji animated?
- expires_at (Optional[str]) - unix timestamp

##### ```gateway.setPlayingStatus```
```python
@bot.gateway.command
def setStatusTest(resp):
    if resp.event.ready_supplemental:
        bot.gateway.setPlayingStatus("Minecraft")
```
###### Parameters:
- game (str)

##### ```gateway.setStreamingStatus```
```python
@bot.gateway.command
def setStatusTest(resp):
    if resp.event.ready_supplemental:
        bot.gateway.setStreamingStatus("pycraft", "https://github.com/ammaraskar/pyCraft")
```
###### Parameters:
- stream (str)
- url (str)

##### ```gateway.setListeningStatus```
```python
@bot.gateway.command
def setStatusTest(resp):
    if resp.event.ready_supplemental:
        bot.gateway.setListeningStatus("pycraft")
```
###### Parameters:
- song (str)

##### ```gateway.setWatchingStatus```
```python
@bot.gateway.command
def setStatusTest(resp):
    if resp.event.ready_supplemental:
        bot.gateway.setWatchingStatus("pycraft")
```
###### Parameters:
- show (str)

##### ```gateway.removePlayingStatus```
```python
@bot.gateway.command
def setStatusTest(resp):
    if resp.event.ready_supplemental:
        bot.gateway.removePlayingStatus()
```
##### ```gateway.removeStreamingStatus```
```python
@bot.gateway.command
def setStatusTest(resp):
    if resp.event.ready_supplemental:
        bot.gateway.removeStreamingStatus()
```
##### ```gateway.removeListeningStatus```
```python
@bot.gateway.command
def setStatusTest(resp):
    if resp.event.ready_supplemental:
        bot.gateway.removeListeningStatus()
```
##### ```gateway.removeWatchingStatus```
```python
@bot.gateway.command
def setStatusTest(resp):
    if resp.event.ready_supplemental:
        bot.gateway.removeWatchingStatus()
```
##### ```gateway.clearActivities```
```python
@bot.gateway.command
def setStatusTest(resp):
    if resp.event.ready_supplemental:
        bot.gateway.clearActivities()
```
##### ```gateway.parse(...).sessions_replace```
```python
bot.gateway.parse(savedEvent).sessions_replace("420420420")
```
where savedEvent is a dictionary with keys ["op", "d", "s", "t"]
###### Parameters
- session_id (Optional[str]) - discord sends this to the client
_____________
### Guild
##### ```gateway.fetchMembers```
[more info](fetchingGuildMembers.md)
```python
bot.gateway.fetchMembers('guildID00000000000', 'channelID00000000000')
bot.gateway.run()
```
###### Parameters:
- guild_id (str)
- channel_id (str) - id of any visible category/channel
- method (str/int/list/tuple) - defaults to "overlap"
  - "overlap":
    - 100 members fetched per request
    - this is how the official discord client fetches the member sidebar (as the user scrolls through the member list)
  - "no overlap"
    - 200 members fetched per request
    - 2 times faster than "overlap" method. However, it's more likely that you'll miss members due to nickname changes and presence updates. Also, it's more likely that you'll get rate-limited while using this method.
  - integer:
    - "overlap" and "no overlap" tell the fetchMembers function to set its multiplier variable to 100 and 200 (ranges are calculated using the multiplier and index values). If you'd like to set a different multiplier, just set method equal to that number. The multiplier has to be a multiple of 100.
  - list/tuple:
    - if you don't want a constant multiplier, set method equal to a list/tuple containing the preferred multipliers in the order that you want them.
- keep (list/str/None) - defaults to []
  - list:
    - all possible member properties are: 
      ```
       ['pending', 'deaf', 'hoisted_role', 'presence', 'joined_at', 'public_flags', 'username', 'avatar', 'discriminator', 'premium_since', 'roles', 'is_pending', 'mute', 'nick', 'bot', 'communication_disabled_until']
      ```
    - set keep to the list of all the member properties you want to retain
    - by default, keep is set to an empty list. This is done to save memory (which really does make a difference for massive guilds).
  - "all":
    - keep all member properties
  - None/[]
    - disregard member properties
- considerUpdates (boolean) - defaults to True
  - presence updates for users come in GUILD_MEMBER_LIST_UPDATE type UPDATE events. For massive guilds (where fetching members can take a while), this can provide updated presence info (only while fetchMembers is running).
  - this param is useless if 'presence' is not in the keep list
- startIndex (integer) - defaults to 0
  - what index to start at. This is useful if fetchMembers doesn't fetch all fetchable members (usually due to rate limiting)
- stopIndex (integer) - defaults to 1000000000
  - what index to stop right before. The stop index is exclusive (like in list slice notation).
- reset (boolean) - defaults to True
  - if you'd like to fetchMembers multiple times without clearing the current member list, set this is False
- wait (float/None) - defaults to None
  - puts a wait time (in seconds) between member fetching requests to prevent getting rate limited
- priority (int) - defaults to 0
  - tells discum where to insert the fetchMembers command

##### ```gateway.getMemberFetchingParams```
(Proof of Concept)
[how to use this function](fetchingGuildMembers.md#fetching-the-member-list-backwards)
```python
startIndex, method = bot.gateway.getMemberFetchingParams([600, 500, 400])
bot.gateway.fetchMembers("guildID","channelID",startIndex=startIndex, method=method, wait=3)
```
The above code will make requests for the following 3 range groups:
```
[[0,99],[600,699],[700,799]] #target start: 600
[[0,99],[500,599],[600,699]] #target start: 500
[[0,99],[400,499],[500,599]] #target start: 400
```
##### ```gateway.finishedMemberFetching```
```python
bot.gateway.finishedMemberFetching('guildID00000000000')
```
###### Parameters:
- guild_id (str)

###### Returns:
boolean

##### ```gateway.findVisibleChannels```
run this either during a gateway connection (after ready_supplemental event) or after a gateway connection
```python
bot.gateway.findVisibleChannels('guildID00000000000')
```

###### Parameters:
- guildID (str)
- types (list) - list of channel types. Defaults to ['guild_text', 'dm', 'guild_voice', 'group_dm', 'guild_category', 'guild_news', 'guild_store', 'guild_news_thread', 'guild_public_thread', 'guild_private_thread', 'guild_stage_voice']
- findFirst (bool) - stop at the first match. Defaults to False

###### Returns:
- list of channel ID string(s)

##### ```gateway.subscribeToGuildEvents```
if you're not receiving events (messages, voice states, etc) from a large guild, then this will fix that
```python
@bot.gateway.command
def subTest(resp):
	if resp.event.ready_supplemental:
		bot.gateway.subscribeToGuildEvents(wait=1)
```

###### Parameters:
- onlyLarge (Optional[bool]) - send opcode 14s to only large guilds (so, less messages sent to discord)
- wait (Optional[int]) - wait time between sending opcode 14s

##### ```gateway.queryGuildMembers```
search for members in guild(s) with a username/nickname that starts with text
```python
@bot.gateway.command
def queryTest(resp):
	if resp.event.ready_supplemental:
		bot.gateway.queryGuildMembers(['guildID'], 'a', limit=100, keep="all")
	if resp.event.guild_members_chunk and bot.gateway.finishedGuildSearch(['guildID'], 'a'): #optional; close gateway after finished
		bot.gateway.close() #optional

bot.gateway.run()

print(bot.gateway.guildMemberSearches['guildID']['queries']['a']) #user IDs of results
print(bot.gateway.session.guild('guildID').members) #member data
```

###### Parameters:
- guildIDs (list) - list of guild ID strings
- query (str) - what to search for
- saveAsQueryOverride (Optional[str]) - save search results under a different query and skip response checking
- limit (Optional[int]) - maximum number of results to return. If you do not have full-memberlist-view perms, the maximum number you can put is 100. Defaults to 10
- presences (Optional[bool]) - include presence data. Defaults to True
- keep (Optional[list/"all"/None]) - what data to save from each member:
  - list:
    - all possible member properties are: 
      ```
       ['pending', 'deaf', 'hoisted_role', 'presence', 'joined_at', 'public_flags', 'username', 'avatar', 'discriminator', 'premium_since', 'roles', 'is_pending', 'mute', 'nick', 'bot']
      ```
    - set keep to the list of all the member properties you want to retain
    - by default, keep is set to an empty list. This is done to save memory (which really does make a different for massive guilds).
  - "all":
    - keep all member properties
  - None
    - disregard member properties

##### ```gateway.checkGuildMembers```
check if user(s) exist in guild(s)
```python
@bot.gateway.command
def checkTest(resp):
	if resp.event.ready_supplemental:
		bot.gateway.checkGuildMembers(['guildID'], ['userID1', 'userID2'], keep="all")
	if resp.event.guild_members_chunk and bot.gateway.finishedGuildSearch(['guildID'], userIDs=['userID1', 'userID2']): #optional; close gateway after finished
		bot.gateway.close() #optional

bot.gateway.run()

print(bot.gateway.guildMemberSearches['guildID']['ids']) #user IDs of results
print(bot.gateway.session.guild('guildID').members) #member data
```

###### Parameters:
- guildIDs (list) - list of guild ID strings
- userIDs (list) - list of user ID strings
- presences (Optional[bool]) - include presence data. Defaults to True
- keep (Optional[list/"all"/None]) - what data to save from each member:
  - list:
    - all possible member properties are: 
      ```
       ['pending', 'deaf', 'hoisted_role', 'presence', 'joined_at', 'public_flags', 'username', 'avatar', 'discriminator', 'premium_since', 'roles', 'is_pending', 'mute', 'nick', 'bot']
      ```
    - set keep to the list of all the member properties you want to retain
    - by default, keep is set to an empty list. This is done to save memory (which really does make a different for massive guilds).
  - "all":
    - keep all member properties
  - None
    - disregard member properties

##### ```gateway.finishedGuildSearch```
```python
print(bot.gateway.finishedGuildSearch(['guildID'], 'a'))
print(bot.gateway.finishedGuildSearch(['guildID'], userIDs=['userID1', 'userID2']))
```

###### Parameters:
put in same parameters as queryGuildMembers or checkGuildMembers
- guildIDs (list) - list of guild ID strings
- query (str)
- saveAsQueryOverride (Optional[str])
- limit (Optional[int])
- presences (Optional[bool])
- keep (Optional[list/"all"/None]) - actually optional

##### ```gateway.request.lazyGuild```
```python
@bot.gateway.command
def guildTest(resp):
    if resp.event.ready_supplemental:
        bot.gateway.request.lazyGuild('guildID000000000', {'channelID0000000': [[0,99]]})
```
###### Parameters:
- guild_id (str)
- channel_ranges (Optional[dict]) - format is {"channelID":ranges} where ranges always contains [0,99] and up to 2 other ranges. So, ```[[0,99]]```, ```[[0,99], [100,199]]```, and ```[[0,99], [100,199], [200,299]]``` are examples of values for ranges
- typing (Optional[bool]) - subscribe to typing indicators
- threads (Optional[bool]) - subscribe to thread updates
- activities (Optional[bool]) - subscribe to activity presence updates
- members (Optional[list]) - list of user id strings. subscribe the guild_member_list_update events from certain user(s)
- thread_member_lists (Optional[list])

##### ```gateway.request.searchGuildMembers```
```python
@bot.gateway.command
def searchGuildMembersTest(resp):
    if resp.event.ready_supplemental:
        bot.gateway.request.searchGuildMembers(['guildID000000000'], "test", 100)
```
###### Parameters:
- guild_ids (list) - list of guild ID strings
- query (Optional[str]) - you can only use query="" on guilds that you have manage server perms on. Defaults to ""
- limit (Optional[int]) - how many users to fetch, can go up to 100. You can only use limit=0 on guilds you have manage server perms on. Defaults to 10
- presences (Optional[bool]) - whether or not to fetch user presences. Defaults to True
- user_ids (Optional[list]) - search if specified users are in guild(s)
- nonce (Optional[str]) - current discord snowflake; user accs don't use this, but it can be helpful for an easy way to link requests to their responses

##### ```gateway.request.searchSlashCommands```
below is an example for sending slash commands to a guild. First we search for slash commands and then we send the one we want.
```python
from discum.utils.slash import SlashCommander

@bot.gateway.command
def slashCommandTest(resp):
    if resp.event.ready_supplemental:
        bot.gateway.request.searchSlashCommands('guildID', limit=10, query="queue")
    if resp.event.guild_application_commands_updated:
        bot.gateway.removeCommand(slashCommandTest)
        slashCmds = resp.parsed.auto()['application_commands']
        s = SlashCommander(slashCmds, application_id='botID')
        data = s.get(['queue'])
        bot.triggerSlashCommand("botID", "channelID", "guildID", data=data)
```
###### Parameters:
- guildID (str)
- query (Optional[str]) - search for commands that start with query
- command_ids (Optional[list]) - list of command ID strings to get data on
- application_id (Optional[str]) - bot ID
- limit (optional[int]) - up to how many results to get. Defaults to 10
- offset (Optional[int]) - start showing results at what index. Defaults to None aka 0
- nonce (Optional[str]) - current discord snowflake. Calculated by default.
- app_type (Optional[str]) - application type. Defaults to 'chat'
| application type | description |
| ----------- | ----------- |
| chat           | Slash commands; a text-based command that shows up when a user types |
| user           | A UI-based command that shows up when you right click or tap on a user |
| message           | A UI-based command that shows up when you right click or tap on a message |

##### ```gateway.parse(...).guild_member_list_update```
```python
bot.gateway.parse(savedEvent).guild_member_list_update
```
where savedEvent is a dictionary with keys ["op", "d", "s", "t"]
##### ```gateway.parse(...).guild_create```
```python
bot.gateway.parse(savedEvent).guild_create("myUserID0000000")
```
where savedEvent is a dictionary with keys ["op", "d", "s", "t"]
###### Parameters:
- my\_user\_id (Optional[str]) - for updating personal role in guild
##### ```gateway.parse(...).guild_members_chunk```
```python
bot.gateway.parse(savedEvent).guild_members_chunk
```
where savedEvent is a dictionary with keys ["op", "d", "s", "t"]
_____________
### Dms
##### ```gateway.request.DMchannel```
```python
@bot.gateway.command
def dmTest(resp):
    if resp.event.ready_supplemental:
        bot.gateway.request.DMchannel("channelID000000000")
```
###### Parameters:
- channelID (str)

_____________
### Channels
##### ```gateway.parse(...).channel_create```
```python
bot.gateway.parse(savedEvent).channel_create
```
where savedEvent is a dictionary with keys ["op", "d", "s", "t"]
##### ```gateway.parse(...).channel_delete```
```python
bot.gateway.parse(savedEvent).channel_delete
```
where savedEvent is a dictionary with keys ["op", "d", "s", "t"]
_____________
### Messages
##### ```gateway.parse(...).message_create```
```python
bot.gateway.parse(savedEvent).message_create
```
where savedEvent is a dictionary with keys ["op", "d", "s", "t"]
_____________
### Media/Calling
##### ```gateway.request.call```
```python
@bot.gateway.command
def callTest(resp):
    if resp.event.ready_supplemental:
        bot.gateway.request.call("channelID000000")
```
###### Parameters:
- channelID (str)
- guildID (Optional[str])
- mute (Optional[bool]) - defaults to False
- deaf (Optional[bool]) - defaults to False
- video (Optional[bool]) - defaults to False
##### ```gateway.request.endCall```
no parameters because client can only be in 1 call (idk yet if this applies to clients connected in multiple sessions)
```python
@bot.gateway.command
def callTest(resp):
    if resp.event.ready_supplemental:
        bot.gateway.request.endCall()
```

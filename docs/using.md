# Using Discum
to make selfbots & userbots
# Table of Contents
- [Quickstart](#Quickstart) 
  - [Installation](#Install)
  - [Initiate client](#Initiate-Client)
  - [Switch logging On/Off](#logging)
  - [Gateway](#Gateway)
- [Messages](#Messages)
- [User Actions](#User-Actions)
- [Guilds](#Guilds)
- [Calling](#Media/Calling)

## Quickstart:
#### Install:
from Github (you can also select a specific release version: https://github.com/Merubokkusu/Discord-S.C.U.M/releases):
```
git clone https://github.com/Merubokkusu/Discord-S.C.U.M.git
cd Discord-S.C.U.M
python setup.py install
```
or from pypi:
```
pip install discum
```
#### Initiate client
```discum.Client(email="", password="", token="", proxy_host=False, proxy_port=False, user_agent="random", log=True)```      
\* note: discord is starting to (sometimes) require captchas for the login (even when not using proxies). Therefore, it's recommended that you provide the email, password, and token (or just the token if you're not using the profile-editing functions).
```python
>>> import discum
>>> bot = discum.Client(email='email@email.com',password='password', log=False)
```
#### Logging
Logging essentially makes discum's communications transparent. All sent data and received (decompressed) data is printed. Purple texts are sent data and green texts are received data. Uncolored texts (usually black or white, depending on your terminal settings) are extra logs.
```python
#for http APIs:
bot.log = True
bot.log = False

#for websocket/gateway APIs:
bot.gateway.log = True
bot.gateway.log = False
```

#### Gateway
##### change commands
```python
#appending/inserting functions to gateway command list
def myfunction(resp):
    pass
bot.gateway.command(function)

or 

@bot.gateway.command
def myfunction(resp):
    pass
'''
you can also set a priority for that function and even pass extra parameters to it (priority & params are optional)
note: resp is always excluded from the params dict
'''
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
```
#remove function from gateway command list
bot.gateway.removeCommand(function)
```
```
#clear gateway command list
bot.gateway.clearCommands()
```
##### connecting & disconnecting
```python
bot.gateway.run(auto_reconnect=True)
bot.gateway.close() #use this while the gateway server is running to close the connection
```
##### resetting current session
Do not run this while the gateway is running. Only run this after you've stopped the gateway server.
```python
bot.gateway.resetSession()
```
##### session data (ready and ready_supplemental)
```python
bot.gateway.session.read()
```
##### auto-parse messages
```python
resp.parsed.auto()
```
## Messages
##### create DM
```createDM(userIDs)```
```python
bot.createDM(['444444444444444444'])
bot.createDM(['222222222222222222','000000000000000000'])
```
##### get messages in a channel
```getMessages(ChannelID,num=1,beforeDate=None,aroundMessage=None)```
```python
bot.getMessages("383003333751856129") #if beforeDate or aroundMessage not given, then most recent message(s) will be returned
```
##### send text message
```sendMessage(ChannelID,message,embed='',tts=False)```
```python
bot.sendMessage("383003333751856129","Hello You :)")
```
* bold message: \*\*text\*\*
* italicized message: \*text\*
* strikethrough message: \~\~text\~\~
* quoted message: \> text
* code: \`text\`
* spoiler: \|\|text\|\|
##### send file
```sendFile(channelID,filelocation,isurl=False,message="")```
```python
bot.sendFile("383003333751856129","https://thiscatdoesnotexist.com/",True)
```
* spoiler images: rename image to SPOILER_imagename.jpg (or whatever extension it has)
##### send embed
```sendMessage(ChannelID,message,embed='',tts=False)```
```python
embed = discum.Embedder()
embed.Title("This is a test")
embed.image('https://cdn.dribbble.com/users/189524/screenshots/2105870/04-example_800x600_v4.gif')
embed.fields('Hello!',':yum:')
embed.fields(':smile:','Testing :)')
embed.author('Tester')
bot.sendMessage("383006063751856129","",embed.read())
```
##### search messages     
(if only guildID is provided, this will return most recent messages in that guild). format 25 grouped results per page, ~4 messages in each group, target messages have key "hit" in them). If you'd like to filter searchMessages to only return the messages you searched for, use filterSearchResults
```searchMessages(guildID,channelID=None,userID=None,mentionsUserID=None,has=None,beforeDate=None,afterDate=None,textSearch=None,afterNumResults=None)```
```python
bot.searchMessages("267624335836053506",textSearch="hello")
```
* params: 
  * channelID,userID,mentionsUserID are lists of either ints or strings
  * has is a list of strings
  * beforeDate and afterDate are ints
  * textSearch is a string
  * afterNumResults is an int (multiples of 25)
##### filter search results
```filterSearchResults(searchResponse)```
```python
searchResponse = bot.searchMessages("267624335836053506",textSearch="hello")
bot.filterSearchResults(searchResponse)
```
##### send typing action
```typingAction(channelID)```
```python
bot.typingAction("267624335836053506")
```
##### delete message
```deleteMessage(channelID,messageID)```
```python
bot.deleteMessage("267624335836053506","711254483669352469")
```
##### edit message
```editMessage(channelID, messageID, newMessage)```
```python
bot.editMessage("267624335836053506","711254483669352469","hi")
```
##### pin message
```pinMessage(channelID,messageID)```
```python
bot.pinMessage("267624335836053506","711254483669352469")
```
##### un-pin message
```unPinMessage(channelID,messageID)```
```python
bot.unPinMessage("267624335836053506","711254483669352469")
```
##### get pinned messages
```getPins(channelID)```
```python
bot.getPins("267624335836053506")
```
##### add reaction
```addReaction(channelID,messageID,emoji)```
```python
bot.addReaction("111111111111111111","222222222222222222","👻")
bot.addReaction("111111111111111111","222222222222222222","wowee:720507026014450205") #emoji name:emoji id
```
##### remove reaction
```removeReaction(channelID,messageID,emoji)```
```python
bot.removeReaction("111111111111111111","222222222222222222","👻")
bot.removeReaction("111111111111111111","222222222222222222","wowee:720507026014450205") #emoji name:emoji id
```
##### acknowledge message (mark message read)
```ackMessage(channelID,messageID,ackToken=None)```
```python
bot.ackMessage("222222222222222222","333333333333333333")
```
- you can technically put any string number (str(num)) as the messageID
##### unacknowledge message (mark message unread)
```unAckMessage(channelID,messageID,numMentions=0)```
```python
bot.unAckMessage("222222222222222222","333333333333333333",250)
```
- numMentions can be any positive integer (but discord registers any input above 250 as 250)      
- you can technically put any string number (str(num)) as the messageID
##### parse message (MESSAGE_CREATE)
```python
resp.parsed.message_create()
```

## User
##### send friend request
```requestFriend(userID)```
```requestFriend(username+"#"+discriminator)```
```python
bot.requestFriend("222222222222222222")
bot.requestFriend("userwow#0001") #random username used here
```
##### accept friend request
```acceptFriend(userID)```
```python
bot.acceptFriend(ID)
```
##### remove friend / unblock user / delete outgoing friend request / reject incoming friend request
```removeRelationship(userID)```
```python
bot.removeRelationship(ID)
```
##### block user
```blockUser(userID)```
```python
bot.blockUser(ID)
```
##### change name
```changeName(name)```
```python
bot.changeName(email,password,name)
```
##### set status
```setStatus(status)```
```python
bot.setStatus(status)
```
##### set avatar
```setAvatar(imagePath)```
```python
bot.setAvatar(email,password,imagePath)
```
##### session (user data)
```python
bot.gateway.session.user
bot.gateway.session.consents
bot.gateway.session.experiments
bot.gateway.session.cachedUsers
bot.gateway.session.mergedPresences
bot.gateway.session.geoOrderedRtcRegions
bot.gateway.session.tutorial #when you create a new acc and discord gives your client a tutorial
bot.gateway.session.readStates
bot.gateway.session.analyticsToken
bot.gateway.session.connectedAccounts
```
##### session (settings)
```python
bot.gateway.session.userSettings
bot.gateway.session.optionsForUserSettings
bot.gateway.session.userGuildSettings
bot.gateway.session.userGuildSetting(guildID).data #for example, notification settings for a guild
```
##### session (relationships)
| Relationship Type | description |
| ------ | ------ |
| 1 | friend |
| 2 | block |
| 3 | incoming friend request |
| 4 | outgoing friend request | 
```python
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
bot.gateway.session.allFriendMergedPresences
bot.gateway.session.allFriendMergedPresenceIDs
bot.gateway.session.friendSuggestionCount
bot.gateway.session.relationship(userID).data
bot.gateway.session.relationship(userID).friendMergedPresenceData
```
##### session (DMs)
```python
bot.gateway.session.DMs
bot.gateway.session.DMIDs
bot.gateway.session.DM(DMID).data
bot.gateway.session.DM(DMID).recipients
```
## Guild
##### get guild info from invite code
```getInfoFromInviteCode(inviteCode)```
```python
bot.getInfoFromInviteCode('1a1a1')
```
##### join guild using invite code
```joinGuild(inviteCode)```
```python
bot.joinGuild('1a1a1')
```
##### kick user
```kick(guildID,userID,reason="")```
```python
bot.kick('guildID00000000000','userID11111111111','weeeee')
bot.kick('guildID00000000000','userID11111111111')
```
##### ban user
```ban(guildID,userID,deleteMessagesDays=0,reason="")```
```python
bot.ban('guildID00000000000','userID11111111111',7,'weeeee')
bot.ban('guildID00000000000','userID11111111111',7)
bot.ban('guildID00000000000','userID11111111111',reason='weeeee')
bot.ban('guildID00000000000','userID11111111111')
```
##### lookup userID in guild \*note: this api endpoint isn't normally used by user accounts
```getGuildMember(guildID,userID)```
```python
bot.getGuildMember('guildID00000000000','userID11111111111')
```
##### fetch guild members
```gateway.fetchMembers(guild_id, channel_id, method="overlap", keep=[], considerUpdates=True, reset=True, wait=None, priority=0)```
```python
bot.gateway.fetchMembers('guildID00000000000', 'channelID00000000000') #all this does is insert a command to fetch members
bot.gateway.run() #you still need to run the gateway to fetch the members
```
Note, if you'd like to close the gateway connection after fetching members, see this [example](https://github.com/Merubokkusu/Discord-S.C.U.M/blob/master/examples/gettingGuildMembers.py).      
Although you technically could request for multiple guilds at the same time, this is not recommended (and you'd likely not get too favorable results from that).
Before explaining the params, here're some things to keep in mind when using this function:
1) There's no actual API endpoint for users to get guild members. [Instead, you have to request for and parse the member list, piece by piece.](https://arandomnewaccount.gitlab.io/discord-unofficial-docs/lazy_guilds.html) The fetchMembers function automates this and automatically removes itself from the command list once finished.
2) Both guild id and channel id need to be provided. The member list is different for each channel. I'd recommend using general, announcements, or rules (some channel that most/everyone has access to).
3) The member list does not necessarily contain all the members. For large guilds, the member list usually does not contain all the members. However, the member list is the most efficient way to get members.
4) Discum's fetchMembers function is coded to mimic the official client behavior for fetching the member list. However, if you'd like to modify fetching behavior, there are params that let you do just that.

params:
- guild_id (str)
- channel_id (str)
- method (str/int/list/tuple):
  - "overlap":
    - fetches member list by requesting for overlapped member ranges (think of it like a sliding window). The member ranges in order of requested are
      ```
      [0,99][100,199]
      [100,199][200,299]
      [200,299][300,399]
      ...
      ```
    - this is how the official discord client fetches the member sidebar (as the user scrolls through the member list)
  - "no overlap"
    - fetches member list by requesting for non-overlapped member ranges. The member ranges in order of requested are
      ```
      [0,99][100,199]
      [200,299][300,399]
      [400,499][500,599]
      ...
      ```
    - 2 times faster than "overlap" method. However, it's more likely that you'll miss members due to nickname changes and presence updates.
  - integer:
    - "overlap" and "no overlap" tell the fetchMembers function to set its multiplier variable to 100 and 200 (ranges are calculated using the multiplier and index values). If you'd like to set a different multiplier, just set method equal to that number. The multiplier has to be a multiple of 100.
  - list/tuple:
    - if you don't want a constant multiplier, set method equal to a list/tuple containing the preferred multipliers in the order that you want them.
- keep (list/str/None):
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
    - an empty list accomplishes the same thing
- considerUpdates (boolean):
  - presence updates for users come in GUILD_MEMBER_LIST_UPDATE type UPDATE events. For massive guilds (where fetching members can take a while), this can provide updated presence info (only while fetchMembers is running).
  - this param is useless if 'presence' is not in the keep list
- reset (boolean):
  - if you'd like to fetchMembers multiple times without clearing the current member list, set this is False
- wait (float/None):
  - if discord disconnects you due to gateway rate limits (normally doesn't happen, but it's possible) and you don't want to try again later, you can set the wait time (in seconds) here. I wouldn't recommend a wait time higher than 1 second. Also, depending on discord's response time, fetchMembers behavior can become unstable if you set a wait time. This parameter should only be used with care.
- priority (int):
  - tells discum where to insert the fetchMembers command. Default priority is 0 for fetchMembers.

##### check member fetching status
```gateway.finishedMemberFetching(guild_id)```
```python
bot.gateway.finishedMemberFetching('guildID00000000000') #returns a boolean
```
for reference, member fetching status data is kept in the ```bot.memberFetchingStatus``` variable.

##### session
```python
bot.gateway.session.guilds
bot.gateway.session.guildExperiments
bot.gateway.session.guildIDs
bot.gateway.session.positions #your roles in each guild. 
bot.gateway.session.guild(guildID).data
bot.gateway.session.guild(guildID).unavailable
bot.gateway.session.guild(guildID).setData #set guild data (and delete existing data)
bot.gateway.session.guild(guildID).modify #update guild data
bot.gateway.session.guild(guildID).hasMembers #checks if members key exists
bot.gateway.session.guild(guildID).members #available after fetchMembers has been run
bot.gateway.session.guild(guildID).resetMembers
bot.gateway.session.guild(guildID).updateOneMember
bot.gateway.session.guild(guildID).updateMembers
bot.gateway.session.guild(guildID).owner
bot.gateway.session.guild(guildID).boostLvl
bot.gateway.session.guild(guildID).emojis
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
bot.gateway.session.guild(guildID).explicitContentFilter
bot.gateway.session.guild(guildID).splashHash
bot.gateway.session.guild(guildID).memberCount
bot.gateway.session.guild(guildID).description
bot.gateway.session.guild(guildID).vanityUrlCode
bot.gateway.session.guild(guildID).preferredLocale
bot.gateway.session.guild(guildID).allChannels
bot.gateway.session.guild(guildID).categories
bot.gateway.session.guild(guildID).categoryIDs
bot.gateway.session.guild(guildID).categoryData(categoryID)
bot.gateway.session.guild(guildID).channels
bot.gateway.session.guild(guildID).channelIDs
bot.gateway.session.guild(guildID).channelData(channelID)
bot.gateway.session.guild(guildID).voiceStates
bot.gateway.session.guild(guildID).notOfflineCachedMembers
bot.gateway.session.guild(guildID).notOfflineCachedMemberIDs
bot.gateway.session.guild(guildID).notOfflineCachedMemberData(userID)
bot.gateway.session.guild(guildID).mergedPresences
bot.gateway.session.guild(guildID).mergedPresenceIDs
bot.gateway.session.guild(guildID).mergedPresenceData(userID)
bot.gateway.session.guild(guildID).position #your roles in a specific guild
```
## Media/Calling
# start call (no function yet for streaming data)
```bot.gateway.request.call(channelID, guildID=None, mute=False, deaf=False, video=False)```
```python
bot.gateway.request.call('channelID000000', guildID=None, mute=False, deaf=False, video=False)
```
# end call
```bot.gateway.request.endCall()```
```python
bot.gateway.request.endCall()
```

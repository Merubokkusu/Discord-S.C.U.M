# Wiki

# Table of Contents
- [Quickstart](#Quickstart)    
- [Messages](#Messages)
- [User Actions](#User-Actions)
- [Guilds](#Guilds)
- [Gateway Server](#Gateway-Server)

## Quickstart:
#### Install:
```
git clone https://github.com/Merubokkusu/Discord-S.C.U.M.git
cd Discord-S.C.U.M
python setup.py install
```
#### Initiate client
```discum.Client(email="none", password="none", token="none", proxy_host=False, proxy_port=False, user_agent="random", log=True)```      
\* note: discord is starting to (sometimes) require captchas for the login. So, in the meanwhile (until we add 2captcha.com support), provide the email, password, and token (or just the token if you're not using the profile-editing functions).
```python
>>> import discum
>>> bot = discum.Client(email='email@email.com',password='password')
'Randomly generated user agent: Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_4 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) CriOS/32.0.1700.20 Mobile/10B350 Safari/8536.25'
 [+] (<discum.login.Login.Login->Connect) Post -> https://discord.com/api/v8/auth/login
 [+] (<discum.login.Login.Login->Connect) {"email": "email@email.com", "password": "password", "undelete": false, "captcha_key": null, "login_source": null, "gift_code_sku_id": null}
 [+] (<discum.login.Login.Login->Connect) Response <- {"token": "420tokentokentokentoken.token.tokentokentokentokentoken", "user_settings": {"locale": "en-US", "theme": "dark"}}
'Retrieving Discord's build number...'
'Discord is currently on build number 71073'
```
#### Turn Logging On/Off (this can be done at any time)
```python
bot.log = True
bot.log = False
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
* input types for the search feature: 
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
## User Actions
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

## Gateway Server
scroll down to view the examples
###### by default, discum initializes the gateway interactions when you first initialize your bot (discum.Client). 
If you'd like to reinitialize the gateway you can:
```python
from discum.gateway.gateway import *
bot.gateway = GatewayServer(bot.websocketurl, token, user_agent_data, proxy_host=None, proxy_port=None, log=True) #user_agent_data is a dictionary with keys: 'os', 'browser' , 'device', 'browser_user_agent', 'browser_version', 'os_version'}
```
###### changing gateway commands
```python
#adding functions to gateway command list
@bot.gateway.command #put ontop of functions you want to run on every received websocket message

#removing functions from gateway command list
bot.gateway.removeCommand(function)

#clearing gateway command list
bot.gateway.clearCommands()
```
###### running and stopping gateway server
```python
bot.gateway.run(auto_reconnect=True)
bot.gateway.close() #this can be done while gateway server is running
```
###### clearing current session (removes data collected from last session)
Do not run this while the gateway is running. Only run this after you've stopped the gateway server.
```python
bot.gateway.resetSession()
```
##### Session Settings
```python
#all settings
bot.gateway.SessionSettings.read()

#user data
bot.gateway.SessionSettings.user

#guild
bot.gateway.SessionSettings.guilds
bot.gateway.SessionSettings.guildIDs
bot.gateway.SessionSettings.positions #your roles in each guild. 
bot.gateway.SessionSettings.guild(guildID).data
bot.gateway.SessionSettings.guild(guildID).owner
bot.gateway.SessionSettings.guild(guildID).boostLvl
bot.gateway.SessionSettings.guild(guildID).emojis
bot.gateway.SessionSettings.guild(guildID).banner
bot.gateway.SessionSettings.guild(guildID).discoverySplash
bot.gateway.SessionSettings.guild(guildID).msgNotificationSettings
bot.gateway.SessionSettings.guild(guildID).rulesChannelID
bot.gateway.SessionSettings.guild(guildID).verificationLvl
bot.gateway.SessionSettings.guild(guildID).features
bot.gateway.SessionSettings.guild(guildID).joinTime
bot.gateway.SessionSettings.guild(guildID).region
bot.gateway.SessionSettings.guild(guildID).applicationID
bot.gateway.SessionSettings.guild(guildID).afkChannelID
bot.gateway.SessionSettings.guild(guildID).icon
bot.gateway.SessionSettings.guild(guildID).name
bot.gateway.SessionSettings.guild(guildID).maxVideoChannelUsers
bot.gateway.SessionSettings.guild(guildID).roles
bot.gateway.SessionSettings.guild(guildID).publicUpdatesChannelID
bot.gateway.SessionSettings.guild(guildID).systemChannelFlags
bot.gateway.SessionSettings.guild(guildID).mfaLvl
bot.gateway.SessionSettings.guild(guildID).afkTimeout
bot.gateway.SessionSettings.guild(guildID).hashes
bot.gateway.SessionSettings.guild(guildID).systemChannelID
bot.gateway.SessionSettings.guild(guildID).lazy
bot.gateway.SessionSettings.guild(guildID).numBoosts
bot.gateway.SessionSettings.guild(guildID).large
bot.gateway.SessionSettings.guild(guildID).explicitContentFilter
bot.gateway.SessionSettings.guild(guildID).splashHash
bot.gateway.SessionSettings.guild(guildID).memberCount
bot.gateway.SessionSettings.guild(guildID).description
bot.gateway.SessionSettings.guild(guildID).vanityUrlCode
bot.gateway.SessionSettings.guild(guildID).preferredLocale
bot.gateway.SessionSettings.guild(guildID).allChannels
bot.gateway.SessionSettings.guild(guildID).categories
bot.gateway.SessionSettings.guild(guildID).categoryIDs
bot.gateway.SessionSettings.guild(guildID).categoryData(categoryID)
bot.gateway.SessionSettings.guild(guildID).channels
bot.gateway.SessionSettings.guild(guildID).channelIDs
bot.gateway.SessionSettings.guild(guildID).channelData(channelID)
bot.gateway.SessionSettings.guild(guildID).voiceStates
bot.gateway.SessionSettings.guild(guildID).notOfflineCachedMembers
bot.gateway.SessionSettings.guild(guildID).notOfflineCachedMemberIDs
bot.gateway.SessionSettings.guild(guildID).notOfflineCachedMemberData(userID)
bot.gateway.SessionSettings.guild(guildID).mergedPresences
bot.gateway.SessionSettings.guild(guildID).mergedPresenceIDs
bot.gateway.SessionSettings.guild(guildID).mergedPresenceData(userID)
bot.gateway.SessionSettings.guild(guildID).position #your roles in a specific guild
```
```python
#relationships
```
| Relationship Type | description |
| ------ | ------ |
| 1 | friend |
| 2 | block |
| 3 | incoming friend request |
| 4 | outgoing friend request | 
```python
bot.gateway.SessionSettings.relationships
bot.gateway.SessionSettings.relationshipIDs
bot.gateway.SessionSettings.friends
bot.gateway.SessionSettings.friendIDs
bot.gateway.SessionSettings.blocked
bot.gateway.SessionSettings.blockedIDs
bot.gateway.SessionSettings.incomingFriendRequests
bot.gateway.SessionSettings.incomingFriendRequestIDs
bot.gateway.SessionSettings.outgoingFriendRequests
bot.gateway.SessionSettings.outgoingFriendRequestIDs
bot.gateway.SessionSettings.allFriendMergedPresences
bot.gateway.SessionSettings.allFriendMergedPresenceIDs
bot.gateway.SessionSettings.relationship(userID).data
bot.gateway.SessionSettings.relationship(userID).friendMergedPresenceData

#DMs
bot.gateway.SessionSettings.DMs
bot.gateway.SessionSettings.DMIDs
bot.gateway.SessionSettings.DM(DMID).data
bot.gateway.SessionSettings.DM(DMID).recipients

#guild settings (like notifications for each guild)
bot.gateway.SessionSettings.userGuildSettings
bot.gateway.SessionSettings.userGuildSetting(guildID).data

#user settings
bot.gateway.SessionSettings.userSettings
bot.gateway.SessionSettings.optionsForUserSettings

#other
bot.gateway.SessionSettings.mergedPresences
bot.gateway.SessionSettings.analyticsToken
bot.gateway.SessionSettings.connectedAccounts
bot.gateway.SessionSettings.consents
bot.gateway.SessionSettings.experiments
bot.gateway.SessionSettings.friendSuggestionCount
bot.gateway.SessionSettings.guildExperiments
bot.gateway.SessionSettings.readStates
bot.gateway.SessionSettings.geoOrderedRtcRegions
bot.gateway.SessionSettings.cachedUsers
bot.gateway.SessionSettings.tutorial
bot.gateway.SessionSettings.mergedPresences
```                               
_______________________
###### Gateway API Examples (assuming you've already imported discum and initialized your bot (bot = discum.Client...))

1)
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
is the same as doing
```python
@bot.gateway.command
def helloworld1(resp):
    if resp['t'] == "READY_SUPPLEMENTAL": #ready_supplemental is sent after ready
        user = bot.gateway.SessionSettings.user
        print("Logged in as {}#{}".format(user['username'], user['discriminator']))

@bot.gateway.command
def helloworld2(resp):
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

2) we can also remove functions
```python
@bot.gateway.command
def example(resp):
    if resp['t'] == "MESSAGE_CREATE":
        print('Detected a message')
        bot.gateway.removeCommand(example) #this works because bot.gateway.command returns the inputted function after adding the function to the command list

bot.gateway.run(auto_reconnect=True)
```
3) clear functions
```python
@bot.gateway.command
def helloworld1(resp):
    if resp['t'] == "READY_SUPPLEMENTAL": #ready_supplemental is sent after ready
        user = bot.gateway.SessionSettings.user
        print("Logged in as {}#{}".format(user['username'], user['discriminator']))

@bot.gateway.command
def helloworld2(resp):
    if resp['t'] == "MESSAGE_CREATE":
        print('Detected a message')
        bot.gateway.clearCommands()

bot.gateway.run(auto_reconnect=True)
```
4) send data
```python
@bot.gateway.command
def sendexample(resp):
    if resp['t'] == "MESSAGE_CREATE":
        print('Detected a message')
        bot.gateway.send({"op":3,"d":{"status":"dnd","since":0,"activities":[],"afk":False}})
        bot.gateway.removeCommand(sendexample) #use this if you only want to send the data once

bot.gateway.run(auto_reconnect=True)
```
5) close connection
```python
@bot.gateway.command
def closeexample(resp):
    if resp['t'] == "MESSAGE_CREATE":
        print('Detected a message')
        bot.gateway.close()

bot.gateway.run(auto_reconnect=True)

bot.gateway.clearCommands() #run this if you want to clear commands
bot.gateway.resetSession() #run this if you want to clear collected session data from last connection
bot.gateway.run(auto_reconnect=True) #and now you can connect to the gateway server again
```

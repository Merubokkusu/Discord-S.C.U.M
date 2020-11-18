![version](https://img.shields.io/badge/github%20version-0.3.0-blue) [![python versions](https://img.shields.io/badge/python-2.7%20%7C%203.5%20%7C%203.6%20%7C%203.7%20%7C%203.8-blue)](https://pypi.org/project/discum/0.2.1/)       
[![PyPI version](https://badge.fury.io/py/discum.svg)](https://badge.fury.io/py/discum) [![python versions](https://img.shields.io/badge/python-3.6%2B-green)](https://pypi.org/project/discum/0.2.1/)


### DisCum: A Discord Selfbot Api Wrapper
using requests and websockets :)

![https://files.catbox.moe/3ns003.png](https://files.catbox.moe/3ns003.png)

\* [changelog](https://github.com/Merubokkusu/Discord-S.C.U.M/blob/master/changelog.md). Updates are slow nowadays due to school and covid and life.        
\* You can send issues to discordtehe@gmail.com (arandomnewaccount will respond). If you put them in the issues tab, either arandomnewaccount will edit your message to "respond" because he can't post public comments or Merubokkusu will respond.
## Info
  Discum is a Discord selfbot api wrapper (in case you didn't know, selfbotting = automating a user account). Whenever you login to discord, your client communicates with Discord's servers using Discord's http api (http(s) requests) and gateway server (websockets). Discum allows you have this communication with Discord with python. 
  
  The main difference between Discum and other Discord api wrapper libraries (like discord.py) is that discum is written and maintained to work on user accounts (so, perfect for selfbots). We thoroughly test all code on here and develop discum to be readable, expandable, and useable.     
  
  Note, using a selfbot is against Discord's Terms of Service and you could get banned for using one if you're not careful. Also, this needs to be said: discum does not have rate limit handling. The main reasons for this are that discum is made to (1) be (relatively) simple and (2) give the developer/user freedom (generally I'd recommend a bit more than 1 second in between tasks of the same type, but if you'd like a longer or shorter wait time that's up to you). We (Merubokkusu and anewrandomaccount) do not take any responsibility for any consequences you might face while using discum. We also do not take any responsibility for any damage caused (to servers/channels) through the use of Discum. Discum is a tool; how you use this tool is on you.

## Install (same on Mac, Linux, Windows, etc)
\* v0.2.8 and before supports python 3.6, 3.7, 3.8 while v0.3.0 supports python 2.7, 3.5, 3.6, 3.7, 3.8      
from source (recommended, up-to-date)(currently on version 0.3.0):      
```
git clone https://github.com/Merubokkusu/Discord-S.C.U.M.git
cd Discord-S.C.U.M
python3 setup.py install               
```
from PyPI:      
```python
pip install discum 
```               
#### Prerequisites (installed automatically using above methods)
- requests
- requests_toolbelt
- websocket_client
- filetype
- user_agents
- random_user_agent

# Usage
### [Read the Wiki](https://github.com/Merubokkusu/Discord-S.C.U.M/blob/master/wiki.md)

# Example
\* note: discord is starting to (sometimes) require captchas for the login. So, in the meanwhile (until we add 2captcha.com support), provide the email, password, and token (or just the token if you're not using the profile-editing functions).
```python
import discum     
bot = discum.Client(token='420tokentokentokentoken.token.tokentokentokentokentoken', log=False)

bot.sendMessage("238323948859439", "Hello :)")

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

### bonus features: 
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
- [X] On-Message (and other on-anything gateway) capabilities
- [ ] Making phone calls, sending audio/video data thru those calls
- [ ] Everything

# Overview (107 functions):
\*replace "bot" with whatever variable name you're using
### Initiate client:
```python
bot = discum.Client(email="none", password="none", token="none", proxy_host=None, proxy_port=None, user_agent="random", log=True)
```
### Http API:
```python
bot.connectionTest(self)
bot.snowflake_to_unixts(snowflake)
bot.unixts_to_snowflake(unixts)

#messages
bot.createDM(recipients)
bot.getMessages(channelID,num=1,beforeDate=None)
bot.sendMessage(channelID,message,embed="",tts=False)
bot.sendFile(channelID,filelocation,isurl=False,message="")
bot.searchMessages(guildID,channelID=None,userID=None,mentionsUserID=None,has=None,beforeDate=None,afterDate=None,textSearch=None,afterNumResults=None)
bot.filterSearchResults(searchResponse)
bot.typingAction(channelID)
bot.deleteMessage(channelID,messageID)
bot.editMessage(channelID,messageID,newMessage)
bot.pinMessage(channelID,messageID)
bot.unPinMessage(channelID,messageID)
bot.addReaction(channelID,messageID,emoji)
bot.removeReaction(channelID,messageID,emoji)
bot.ackMessage(channelID,messageID,ackToken=None)
bot.unAckMessage(channelID,messageID,numMentions=0)
bot.getPins(channelID)

#user
bot.requestFriend(user)
bot.acceptFriend(userID)
bot.removeRelationship(userID)
bot.blockUser(userID)
bot.changeName(name)
bot.setStatus(status)
bot.setAvatar(imagePath)

#guild/server
bot.getInfoFromInviteCode(inviteCode)
bot.joinGuild(inviteCode)
bot.kick(guildID,userID,reason="")
bot.ban(guildID,userID,deleteMessagesDays=0,reason="")
bot.getGuildMember(guildID,userID) #endpoint not actually used by official discord client
```        
### Gateway API:
##### by default, discum initializes the gateway interactions when you first initialize your bot (discum.Client). 
If you'd like to reinitialize the gateway you can:
```python
from discum.gateway.gateway import *
bot.gateway = GatewayServer(bot.websocketurl, token, user_agent_data, proxy_host=None, proxy_port=None, log=True) #user_agent_data is a dictionary with keys: 'os', 'browser' , 'device', 'browser_user_agent', 'browser_version', 'os_version'}
```
##### changing gateway commands
```python
#adding functions to gateway command list
@bot.gateway.command #put ontop of functions you want to run on every received websocket message

#removing functions from gateway command list
bot.gateway.removeCommand(function)

#clearing gateway command list
bot.gateway.clearCommands()
```
##### send data (run while connected to gateway)
```python
bot.gateway.send(data)
```
##### running and stopping gateway server
```python
bot.gateway.run(auto_reconnect=True)
bot.gateway.close() #this can be done while gateway server is running
```
##### clearing current session (removes data collected from last session)
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

#relationships
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
### Contributions?
Contributions are always welcome! Feel free to submit issues or suggest features! Ofc not all suggestions will be implemented (because discum is intended to be a transparent, relatively-raw discord user api wrapper), but all suggestions will be looked into.           

### Contributions:
Here's a list of other ppl who've contributed some code to discum:
- Echocage:
     ```python
     bot.getGuildMember(guildID,userID)
     ```
- ImperialCrise: found an error in discum.py (runIt needed to be changed to run) (helped to debug code right before a release)

### Notes:
In recent years, token logging has become more common (as many people don't check code before they run it). I've seen many closed-source selfbots, and while surely some are well intentioned, others not so much. Discum (discord api wrapper) is open-sourced and organized to provide transparency, but even so, we encourage you to look at the code. Not only will looking at the code help you to better understand how discord's api is structured, but it'll also let you know exactly what you're running. If you have any questions about Discum, feel free to ask us.

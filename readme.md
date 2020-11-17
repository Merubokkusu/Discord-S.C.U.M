![version](https://img.shields.io/badge/version-0.3.0-blue) [![PyPI version](https://badge.fury.io/py/discum.svg)](https://badge.fury.io/py/discum) [![python versions](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue)](https://pypi.org/project/discum/0.2.1/)


### DisCum: A Discord Selfbot Api Wrapper
using requests and websockets :)

![https://files.catbox.moe/3ns003.png](https://files.catbox.moe/3ns003.png)

\* [changelog](https://github.com/Merubokkusu/Discord-S.C.U.M/blob/master/changelog.md). Updates are slow nowadays due to school and covid and life.        
\* You can send issues to discordtehe@gmail.com (arandomnewaccount will respond). If you put them in the issues tab, either arandomnewaccount will edit your message to "respond" because he can't post public comments or Merubokkusu will respond.
## Info
  Discum is a Discord selfbot api wrapper (in case you didn't know, selfbotting = automating a user account). Whenever you login to discord, your client communicates with Discord's servers using Discord's http api (http(s) requests) and gateway server (websockets). Discum allows you have this communication with Discord with python. 
  
  The main difference between Discum and other Discord api wrapper libraries (like discord.py) is that discum is written and maintained to work on user accounts (so, perfect for selfbots). We thoroughly test all code on here and develop discum to be readable, expandable, and useable.     
  
  Note, using a selfbot is against Discord's Terms of Service and you could get banned for using one if you're not careful. Also, this needs to be said: discum does not have rate limit handling. The main reasons for this are that discum is made to (1) be (relatively) simple and (2) give the developer/user freedom (generally I'd recommend a bit more than 1 second in between tasks of the same type, but if you'd like a longer or shorter wait time that's up to you). We (Merubokkusu and anewrandomaccount) do not take any responsibility for any consequences you might face while using discum. We also do not take any responsibility for any damage caused (to servers/channels) through the use of Discum. Discum is a tool; how you use this tool is on you.

## Install (installation should be the same on Mac, Linux, Windows, etc; just make sure you're using python 3.6+)
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
        print(f"Logged in as {user['username']}#{user['discriminator']}")
    if resp['t'] == "MESSAGE_CREATE":
        m = resp['d']
        print(f"> guild {m['guild_id'] if 'guild_id' in m else None} channel {m['channel_id']} | {m['author']['username']}#{m['author']['discriminator']}: {m['content']}")

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

# Overview (106 functions):

### Initiate client:
```python
discum.Client(email="none", password="none", token="none", proxy_host=None, proxy_port=None, user_agent="random", log=True)
```
### Http API:
```python
connectionTest(self)
snowflake_to_unixts(snowflake)
unixts_to_snowflake(unixts)
createDM(recipients)
getMessages(channelID,num=1,beforeDate=None)
sendMessage(channelID,message,embed="",tts=False)
sendFile(channelID,filelocation,isurl=False,message="")
searchMessages(guildID,channelID=None,userID=None,mentionsUserID=None,has=None,beforeDate=None,afterDate=None,textSearch=None,afterNumResults=None)
filterSearchResults(searchResponse)
typingAction(channelID)
deleteMessage(channelID,messageID)
editMessage(channelID,messageID,newMessage)
pinMessage(channelID,messageID)
unPinMessage(channelID,messageID)
addReaction(channelID,messageID,emoji)
removeReaction(channelID,messageID,emoji)
ackMessage(channelID,messageID,ackToken=None)
unAckMessage(channelID,messageID,numMentions=0)
getPins(channelID)
requestFriend(user)
acceptFriend(userID)
removeRelationship(userID)
blockUser(userID)
changeName(name)
setStatus(status)
setAvatar(imagePath)
getInfoFromInviteCode(inviteCode)
joinGuild(inviteCode)
kick(guildID,userID,reason="")
ban(guildID,userID,deleteMessagesDays=0,reason="")
getGuildMember(guildID,userID) #endpoint not actually used by official discord client
```        
### Gateway API:
##### by default, discum initializes the gateway interactions when you first initialize your bot (discum.Client). 
If you'd like to reinitialize the gateway you can (replace "bot" with whatever variable name you're using):
```python
from discum.gateway.gateway import *
bot.gateway = GatewayServer(bot.websocketurl, token, user_agent_data, proxy_host, proxy_port, log) #user_agent_data is a dictionary with keys: 'os', 'browser' , 'device', 'browser_user_agent', 'browser_version', 'os_version'}
```
##### changing gateway commands
```python
#adding functions to gateway command list
@bot.gateway.command #put ontop of functions you want to run on every received websocket message (replace "bot" with whatever variable name you're using)

#removing functions from gateway command list
gateway.removeCommand(function)

#clearing gateway command list
gateway.clearCommands()
```
##### running and stopping gateway server
```python
gateway.run(auto_reconnect=True)
gateway.close() #this can be done while gateway server is running
```
##### clearing current session (removes data collected from last session)
Do not run this while the gateway is running. Only run this after you've stopped the gateway server.
```python
bot.gateway.resetSession()
```
##### Session Settings
```python
#all settings
gateway.SessionSettings.read()

#user data
gateway.SessionSettings.user

#guilds
gateway.SessionSettings.guilds
gateway.SessionSettings.guildIDs
gateway.SessionSettings.positions #your roles in each guild. 
gateway.SessionSettings.guild(guildID).data
gateway.SessionSettings.guild(guildID).owner
gateway.SessionSettings.guild(guildID).boostLvl
gateway.SessionSettings.guild(guildID).emojis
gateway.SessionSettings.guild(guildID).banner
gateway.SessionSettings.guild(guildID).discoverySplash
gateway.SessionSettings.guild(guildID).msgNotificationSettings
gateway.SessionSettings.guild(guildID).rulesChannelID
gateway.SessionSettings.guild(guildID).verificationLvl
gateway.SessionSettings.guild(guildID).features
gateway.SessionSettings.guild(guildID).joinTime
gateway.SessionSettings.guild(guildID).region
gateway.SessionSettings.guild(guildID).applicationID
gateway.SessionSettings.guild(guildID).afkChannelID
gateway.SessionSettings.guild(guildID).icon
gateway.SessionSettings.guild(guildID).name
gateway.SessionSettings.guild(guildID).maxVideoChannelUsers
gateway.SessionSettings.guild(guildID).roles
gateway.SessionSettings.guild(guildID).publicUpdatesChannelID
gateway.SessionSettings.guild(guildID).systemChannelFlags
gateway.SessionSettings.guild(guildID).mfaLvl
gateway.SessionSettings.guild(guildID).afkTimeout
gateway.SessionSettings.guild(guildID).hashes
gateway.SessionSettings.guild(guildID).systemChannelID
gateway.SessionSettings.guild(guildID).lazy
gateway.SessionSettings.guild(guildID).numBoosts
gateway.SessionSettings.guild(guildID).large
gateway.SessionSettings.guild(guildID).explicitContentFilter
gateway.SessionSettings.guild(guildID).splashHash
gateway.SessionSettings.guild(guildID).memberCount
gateway.SessionSettings.guild(guildID).description
gateway.SessionSettings.guild(guildID).vanityUrlCode
gateway.SessionSettings.guild(guildID).preferredLocale
gateway.SessionSettings.guild(guildID).allChannels
gateway.SessionSettings.guild(guildID).categories
gateway.SessionSettings.guild(guildID).categoryIDs
gateway.SessionSettings.guild(guildID).categoryData(categoryID)
gateway.SessionSettings.guild(guildID).channels
gateway.SessionSettings.guild(guildID).channelIDs
gateway.SessionSettings.guild(guildID).channelData(channelID)
gateway.SessionSettings.guild(guildID).voiceStates
gateway.SessionSettings.guild(guildID).notOfflineCachedMembers
gateway.SessionSettings.guild(guildID).notOfflineCachedMemberIDs
gateway.SessionSettings.guild(guildID).notOfflineCachedMemberData(userID)
gateway.SessionSettings.guild(guildID).mergedPresences
gateway.SessionSettings.guild(guildID).mergedPresenceIDs
gateway.SessionSettings.guild(guildID).mergedPresenceData(userID)
gateway.SessionSettings.guild(guildID).position #your roles in a specific guild

#relationships
gateway.SessionSettings.relationships
gateway.SessionSettings.relationshipIDs
gateway.SessionSettings.friends
gateway.SessionSettings.friendIDs
gateway.SessionSettings.blocked
gateway.SessionSettings.blockedIDs
gateway.SessionSettings.incomingFriendRequests
gateway.SessionSettings.incomingFriendRequestIDs
gateway.SessionSettings.outgoingFriendRequests
gateway.SessionSettings.outgoingFriendRequestIDs
gateway.SessionSettings.allFriendMergedPresences
gateway.SessionSettings.allFriendMergedPresenceIDs
gateway.SessionSettings.relationship(userID).data
gateway.SessionSettings.relationship(userID).friendMergedPresenceData

#DMs
gateway.SessionSettings.DMs
gateway.SessionSettings.DMIDs
gateway.SessionSettings.DM(DMID).data
gateway.SessionSettings.DM(DMID).recipients

#guild settings (like notifications for each guild)
gateway.SessionSettings.userGuildSettings
gateway.SessionSettings.userGuildSetting(guildID).data

#user settings
gateway.SessionSettings.userSettings
gateway.SessionSettings.optionsForUserSettings

#other
gateway.SessionSettings.mergedPresences
gateway.SessionSettings.analyticsToken
gateway.SessionSettings.connectedAccounts
gateway.SessionSettings.consents
gateway.SessionSettings.experiments
gateway.SessionSettings.friendSuggestionCount
gateway.SessionSettings.guildExperiments
gateway.SessionSettings.readStates
gateway.SessionSettings.geoOrderedRtcRegions
gateway.SessionSettings.cachedUsers
gateway.SessionSettings.tutorial
gateway.SessionSettings.mergedPresences
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

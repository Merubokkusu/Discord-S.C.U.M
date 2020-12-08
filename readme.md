# DisCum
![version](https://img.shields.io/badge/github%20version-0.3.0-blue) [![python versions](https://img.shields.io/badge/python-2.7%20%7C%203.5%20%7C%203.6%20%7C%203.7%20%7C%203.8-blue)](https://pypi.org/project/discum/0.2.1/)       
[![PyPI version](https://badge.fury.io/py/discum.svg)](https://badge.fury.io/py/discum) [![python versions](https://img.shields.io/badge/python-2.7%20%7C%203.5%20%7C%203.6%20%7C%203.7%20%7C%203.8-green)](https://pypi.org/project/discum/0.2.1/)      
A simple, easy to use, non-restrictive Discord API Wrapper written in Python.       
-using requests and websockets :)

![https://files.catbox.moe/3ns003.png](https://files.catbox.moe/3ns003.png)
        
\* You can send issues to discordtehe@gmail.com (arandomnewaccount will respond). If you put them in the issues tab, either arandomnewaccount will edit your message to "respond" because he can't post public comments or Merubokkusu will respond.

## Table of Contents
- [About](#About)
- [Installation](#Installation)
  - [Prerequisites](#Prerequisites)
- [Example Usage](#Example-usage)
- [Links](#Links)
- [To Do](#To-Do)
- [Summary](#Summary)
- [Contributing](#Contributing)
- [Notes](#Notes)

## About
  Discum is a Discord selfbot api wrapper (in case you didn't know, selfbotting = automating a user account). Whenever you login to discord, your client communicates with Discord's servers using Discord's http api (http(s) requests) and gateway server (websockets). Discum allows you have this communication with Discord with python. 
  
  The main difference between Discum and other Discord api wrapper libraries (like discord.py) is that discum is written and maintained to work on user accounts (so, perfect for selfbots). We thoroughly test all code on here and develop discum to be readable, expandable, and useable.     
  
  Note, using a selfbot is against Discord's Terms of Service and you could get banned for using one if you're not careful. Also, this needs to be said: discum does not have rate limit handling. The main reasons for this are that discum is made to (1) be (relatively) simple and (2) give the developer/user freedom (generally I'd recommend a bit more than 1 second in between tasks of the same type, but if you'd like a longer or shorter wait time that's up to you). We (Merubokkusu and anewrandomaccount) do not take any responsibility for any consequences you might face while using discum. We also do not take any responsibility for any damage caused (to servers/channels) through the use of Discum. Discum is a tool; how you use this tool is on you.

## Installation    
```
git clone https://github.com/Merubokkusu/Discord-S.C.U.M.git
cd Discord-S.C.U.M
python setup.py install               
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

# Example usage
```python
import discum     
bot = discum.Client(token='420tokentokentokentoken.token.tokentokentokentokentoken', log=False)

bot.sendMessage("238323948859439", "Hello :)")

@bot.gateway.command
def helloworld(resp):
    if resp['t'] == "READY_SUPPLEMENTAL": #ready_supplemental is sent after ready
        user = bot.gateway.session.user
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

# Links
[Documentation](https://github.com/Merubokkusu/Discord-S.C.U.M/blob/master/wiki.md)      
[Changelog](https://github.com/Merubokkusu/Discord-S.C.U.M/blob/master/changelog.md)      
[GitHub](https://github.com/Merubokkusu/Discord-S.C.U.M)      
[PyPi](https://pypi.org/project/discum/)      

# To Do
- [x] Sending basic text messages
- [X] Sending Images
- [x] Sending Embeds
- [X] Sending Requests (Friends etc)
- [X] Profile Editing (Name,Status,Avatar)
- [X] On-Message (and other on-anything gateway) capabilities
- [ ] Getting guild members
- [ ] Making phone calls, sending audio/video data thru those calls
- [ ] bypass fingerprint detection? maybe?
- [ ] Everything

# Summary:
\*added a few functions but im kinda tired rn so ill update the readme and wiki tmr
>107 functions:      
>(\*replace "bot" with whatever variable name you're using)
>### Initiate client:
>```python
>bot = discum.Client(email="none", password="none", token="none", proxy_host=None, proxy_port=None, user_agent="random", log=True)
>```
>### Http API:
>```python
>bot.connectionTest(self)
>bot.snowflake_to_unixts(snowflake) #unixts is of type int
>bot.unixts_to_snowflake(unixts) #snowflake is of type int
>
>#messages
>bot.createDM(recipients)
>bot.getMessages(channelID,num=1,beforeDate=None)
>bot.sendMessage(channelID,message,embed="",tts=False)
>bot.sendFile(channelID,filelocation,isurl=False,message="")
>bot.searchMessages(guildID,channelID=None,userID=None,mentionsUserID=None,has=None,beforeDate=None,afterDate=None,textSearch=None,afterNumResults=None)
>bot.filterSearchResults(searchResponse)
>bot.typingAction(channelID)
>bot.deleteMessage(channelID,messageID)
>bot.editMessage(channelID,messageID,newMessage)
>bot.pinMessage(channelID,messageID)
>bot.unPinMessage(channelID,messageID)
>bot.addReaction(channelID,messageID,emoji)
>bot.removeReaction(channelID,messageID,emoji)
>bot.ackMessage(channelID,messageID,ackToken=None)
>bot.unAckMessage(channelID,messageID,numMentions=0)
>bot.getPins(channelID)
>
>#user
>bot.requestFriend(user)
>bot.acceptFriend(userID)
>bot.removeRelationship(userID)
>bot.blockUser(userID)
>bot.changeName(name)
>bot.setStatus(status)
>bot.setAvatar(imagePath)
>
>#guild/server
>bot.getInfoFromInviteCode(inviteCode)
>bot.joinGuild(inviteCode)
>bot.kick(guildID,userID,reason="")
>bot.ban(guildID,userID,deleteMessagesDays=0,reason="")
>bot.getGuildMember(guildID,userID) #endpoint not actually used by official discord client
>```        
>### Gateway API:
>##### by default, discum initializes the gateway interactions when you first initialize your bot (discum.Client). 
>If you'd like to reinitialize the gateway you can:
>```python
>from discum.gateway.gateway import *
>bot.gateway = GatewayServer(bot.websocketurl, token, user_agent_data, proxy_host=None, proxy_port=None, log=True) #user_agent_data is a dictionary with keys: >'os', 'browser' , 'device', 'browser_user_agent', 'browser_version', 'os_version'}
>```
>##### changing gateway commands
>```python
>#adding functions to gateway command list
>@bot.gateway.command #put ontop of functions you want to run on every received websocket message
>
>#removing functions from gateway command list
>bot.gateway.removeCommand(function)
>
>#clearing gateway command list
>bot.gateway.clearCommands()
>```
>##### send data (run while connected to gateway)
>```python
>bot.gateway.send(data)
>```
>##### running and stopping gateway server
>```python
>bot.gateway.run(auto_reconnect=True)
>bot.gateway.close() #this can be done while gateway server is running
>```
>##### clearing current session (removes data collected from last session)
>Do not run this while the gateway is running. Only run this after you've stopped the gateway server.
>```python
>bot.gateway.resetSession()
>```
>##### Session Settings
>```python
>#all settings
>bot.gateway.session.read()
>
>#user data
>bot.gateway.session.user
>
>#guild
>bot.gateway.session.guilds
>bot.gateway.session.guildIDs
>bot.gateway.session.positions #your roles in each guild. 
>bot.gateway.session.guild(guildID).data
>bot.gateway.session.guild(guildID).unavailable
>bot.gateway.session.guild(guildID).setData
>bot.gateway.session.guild(guildID).modify
>bot.gateway.session.guild(guildID).someMembers #only works on guilds you've joined after you've connected
>bot.gateway.session.guild(guildID).owner
>bot.gateway.session.guild(guildID).boostLvl
>bot.gateway.session.guild(guildID).emojis
>bot.gateway.session.guild(guildID).banner
>bot.gateway.session.guild(guildID).discoverySplash
>bot.gateway.session.guild(guildID).msgNotificationSettings
>bot.gateway.session.guild(guildID).rulesChannelID
>bot.gateway.session.guild(guildID).verificationLvl
>bot.gateway.session.guild(guildID).features
>bot.gateway.session.guild(guildID).joinTime
>bot.gateway.session.guild(guildID).region
>bot.gateway.session.guild(guildID).applicationID
>bot.gateway.session.guild(guildID).afkChannelID
>bot.gateway.session.guild(guildID).icon
>bot.gateway.session.guild(guildID).name
>bot.gateway.session.guild(guildID).maxVideoChannelUsers
>bot.gateway.session.guild(guildID).roles
>bot.gateway.session.guild(guildID).publicUpdatesChannelID
>bot.gateway.session.guild(guildID).systemChannelFlags
>bot.gateway.session.guild(guildID).mfaLvl
>bot.gateway.session.guild(guildID).afkTimeout
>bot.gateway.session.guild(guildID).hashes
>bot.gateway.session.guild(guildID).systemChannelID
>bot.gateway.session.guild(guildID).lazy
>bot.gateway.session.guild(guildID).numBoosts
>bot.gateway.session.guild(guildID).large
>bot.gateway.session.guild(guildID).explicitContentFilter
>bot.gateway.session.guild(guildID).splashHash
>bot.gateway.session.guild(guildID).memberCount
>bot.gateway.session.guild(guildID).description
>bot.gateway.session.guild(guildID).vanityUrlCode
>bot.gateway.session.guild(guildID).preferredLocale
>bot.gateway.session.guild(guildID).allChannels
>bot.gateway.session.guild(guildID).categories
>bot.gateway.session.guild(guildID).categoryIDs
>bot.gateway.session.guild(guildID).categoryData(categoryID)
>bot.gateway.session.guild(guildID).channels
>bot.gateway.session.guild(guildID).channelIDs
>bot.gateway.session.guild(guildID).channelData(channelID)
>bot.gateway.session.guild(guildID).voiceStates
>bot.gateway.session.guild(guildID).notOfflineCachedMembers
>bot.gateway.session.guild(guildID).notOfflineCachedMemberIDs
>bot.gateway.session.guild(guildID).notOfflineCachedMemberData(userID)
>bot.gateway.session.guild(guildID).mergedPresences
>bot.gateway.session.guild(guildID).mergedPresenceIDs
>bot.gateway.session.guild(guildID).mergedPresenceData(userID)
>bot.gateway.session.guild(guildID).position #your roles in a specific guild
>
>#relationships
>bot.gateway.session.relationships
>bot.gateway.session.relationshipIDs
>bot.gateway.session.friends
>bot.gateway.session.friendIDs
>bot.gateway.session.blocked
>bot.gateway.session.blockedIDs
>bot.gateway.session.incomingFriendRequests
>bot.gateway.session.incomingFriendRequestIDs
>bot.gateway.session.outgoingFriendRequests
>bot.gateway.session.outgoingFriendRequestIDs
>bot.gateway.session.allFriendMergedPresences
>bot.gateway.session.allFriendMergedPresenceIDs
>bot.gateway.session.relationship(userID).data
>bot.gateway.session.relationship(userID).friendMergedPresenceData
>
>#DMs
>bot.gateway.session.DMs
>bot.gateway.session.DMIDs
>bot.gateway.session.DM(DMID).data
>bot.gateway.session.DM(DMID).recipients
>
>#guild settings (like notifications for each guild)
>bot.gateway.session.userGuildSettings
>bot.gateway.session.userGuildSetting(guildID).data
>
>#user settings
>bot.gateway.session.userSettings
>bot.gateway.session.optionsForUserSettings
>
>#other
>bot.gateway.session.mergedPresences
>bot.gateway.session.analyticsToken
>bot.gateway.session.connectedAccounts
>bot.gateway.session.consents
>bot.gateway.session.experiments
>bot.gateway.session.friendSuggestionCount
>bot.gateway.session.guildExperiments
>bot.gateway.session.readStates
>bot.gateway.session.geoOrderedRtcRegions
>bot.gateway.session.cachedUsers
>bot.gateway.session.tutorial
>bot.gateway.session.mergedPresences
>```
## Contributing
Contributions are welcome. You can submit issues, make pull requests, or suggest features. Ofc not all suggestions will be implemented (because discum is intended to be a transparent, relatively-raw discord user api wrapper), but all suggestions will be looked into.            

## Notes:
In recent years, token logging has become more common (as many people don't check code before they run it). I've seen many closed-source selfbots, and while surely some are well intentioned, others not so much. Discum (discord api wrapper) is open-sourced and organized to provide transparency, but even so, we encourage you to look at the code. Not only will looking at the code help you to better understand how discord's api is structured, but it'll also let you know exactly what you're running. If you have any questions about Discum, feel free to ask us.

![version](https://img.shields.io/badge/version-0.2.5-blue) [![PyPI version](https://badge.fury.io/py/discum.svg)](https://badge.fury.io/py/discum) [![python versions](https://img.shields.io/badge/python-3.7%20%7C%203.8-blue)](https://pypi.org/project/discum/0.2.1/) [![Downloads](https://pepy.tech/badge/discum/month)](https://pepy.tech/project/discum/month)


### A Discord Selfbot Api Wrapper - discum

![https://files.catbox.moe/3ns003.png](https://files.catbox.moe/3ns003.png)

\* [changelog](https://github.com/Merubokkusu/Discord-S.C.U.M/blob/master/changelog.md). Updates are slow nowadays due to school and covid and life.        
\* You can send issues to discordtehe@gmail.com (arandomnewaccount will respond). If you put them in the issues tab, either arandomnewaccount will edit your message to "respond" because he can't post public comments or Merubokkusu will respond.
## Info
  Discum is a Discord selfbot api wrapper (in case you didn't know, selfbotting = automating a user account). Whenever you login to discord, your client communicates with Discord's servers using Discord's http api (http(s) requests) and gateway server (websockets). Discum allows you have this communication with Discord with python. 
  
  The main difference between Discum and other Discord api wrapper libraries (like discord.py) is that discum is written and maintained to work on user accounts (so, perfect for selfbots). We thoroughly test all code on here and develop discum to be readable, expandable, and useable.     
  
  Note, using a selfbot is against Discord's Terms of Service and you could get banned for using one if you're not careful. Also, this needs to be said: discum does not have rate limit handling. The main reasons for this are that discum is made to (1) be (relatively) simple and (2) give the developer/user freedom (generally I'd recommend a bit more than 1 second in between tasks of the same type, but if you'd like a longer or shorter wait time that's up to you). We (Merubokkusu and anewrandomaccount) do not take any responsibility for any consequences you might face while using discum. We also do not take any responsibility for any damage caused (to servers/channels) through the use of Discum. Discum is a tool; how you use this tool is on you.

## Install (installation should be the same on Mac, Linux, Windows, etc; just make sure you're using python 3.7 or 3.8)
from PyPI (this is probably outdated, installing from source is recommended):      
```python
pip install discum 
```
     
from source (this is up-to-date with recent changes)(currently on version 0.2.5):      
```
git clone https://github.com/Merubokkusu/Discord-S.C.U.M.git
cd Discord-S.C.U.M
python3 setup.py install               
```

# Usage
### [Read the Wiki](https://github.com/Merubokkusu/Discord-S.C.U.M/blob/master/wiki.md)

# Example
```python
import discum     
bot = discum.Client(email=,password=,log=True) #note, this will not work if you have a MFA account
#bot = discum.Client(email=,password=,proxy_host=,proxy_port=,user_agent=,log=False)
#bot = discum.Client(email=,password=,token=,log=False) #works for all types of accounts
#bot = discum.Client(token=,log=True) #works for all types of accounts, no profile editing however
#bot = discum.Client(token=,proxy_host=,proxy_port=) #works for all types of accounts, no profile editing however
bot.read()
bot.read(update=False)
bot.getGuildIDs(update=False)
bot.log=False
bot.sendMessage("383003333751856129","Hello You :)")
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
- [ ] Making phone calls, sending audio/video data thru those calls
- [ ] Everything

# list of all 64 functions (click thru these and github should show their location in discum.py)
\* turns out I was accidently double-counting some functions before. Apologies, I hadn't noticed till now.
```python
discum.Client(email="none", password="none", token="none", proxy_host=False, proxy_port=False, user_agent="random",log=True) #look at __init__
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
getGuildVoiceStates(guildID,update=True)
getGuildCachedMembers(guildID,update=True)
getGuildCachedMemberIDs(guildID,update=True)
getGuildCachedMemberData(guildID,memberID,update=True)
getNotes(update=True)
getOnlineFriends(update=True)
getDMs(update=True)
getDMIDs(update=True)
getDMData(DMID,update=True)
getDMRecipients(DMID,update=True)
getReadStates(update=True)
getRelationships(update=True)
getRelationshipIDs(update=True)
getRelationshipData(userID,update=True)
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
_Client__gateway_server.runIt(data,log) #for websocket connections
getInfoFromInviteCode(inviteCode)
joinGuild(inviteCode)
kick(guildID,userID,reason="")
ban(guildID,userID,deleteMessagesDays=0,reason="")
getGuildMember(guildID,userID) #get guild member data
```        
### Contributions?
Contributions are always welcome! Feel free to submit issues or suggest features! Also if you've worked with websockets + async in python before and would like to help out, let us know (GatewayServer.py is kind of a mess rn ngl lol). Ofc not all suggestions will be implemented (because discum is intended to be a transparent, raw discord user api wrapper), but all suggestions will be looked into.           

### Contributions:
Here's a list of other ppl who've contributed something to discum:
- Echocage: api endpoint for 
     ```python
     bot.getGuildMember(guildID,userID)
     ```

### Notes:
In recent years, token logging has become more common (as many people don't check code before they run it). I've seen many closed-source selfbots, and while surely some are well intentioned, others not so much. Discum (discord api wrapper) is open-sourced and organized to provide transparency, but even so, we encourage you to look at the code. Not only will looking at the code help you to better understand how discord's api is structured, but it'll also let you know exactly what you're running. If you have any questions about Discum, feel free to ask us.

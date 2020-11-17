![version](https://img.shields.io/badge/version-0.3.0-blue) [![PyPI version](https://badge.fury.io/py/discum.svg)](https://badge.fury.io/py/discum) [![python versions](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue)](https://pypi.org/project/discum/0.2.1/)


### A Discord Selfbot Api Wrapper - discum

![https://files.catbox.moe/3ns003.png](https://files.catbox.moe/3ns003.png)

\* [changelog](https://github.com/Merubokkusu/Discord-S.C.U.M/blob/master/changelog.md). Updates are slow nowadays due to school and covid and life.        
\* You can send issues to discordtehe@gmail.com (arandomnewaccount will respond). If you put them in the issues tab, either arandomnewaccount will edit your message to "respond" because he can't post public comments or Merubokkusu will respond.
## Info
  Discum is a Discord selfbot api wrapper (in case you didn't know, selfbotting = automating a user account). Whenever you login to discord, your client communicates with Discord's servers using Discord's http api (http(s) requests) and gateway server (websockets). Discum allows you have this communication with Discord with python. 
  
  The main difference between Discum and other Discord api wrapper libraries (like discord.py) is that discum is written and maintained to work on user accounts (so, perfect for selfbots). We thoroughly test all code on here and develop discum to be readable, expandable, and useable.     
  
  Note, using a selfbot is against Discord's Terms of Service and you could get banned for using one if you're not careful. Also, this needs to be said: discum does not have rate limit handling. The main reasons for this are that discum is made to (1) be (relatively) simple and (2) give the developer/user freedom (generally I'd recommend a bit more than 1 second in between tasks of the same type, but if you'd like a longer or shorter wait time that's up to you). We (Merubokkusu and anewrandomaccount) do not take any responsibility for any consequences you might face while using discum. We also do not take any responsibility for any damage caused (to servers/channels) through the use of Discum. Discum is a tool; how you use this tool is on you.

## Install (installation should be the same on Mac, Linux, Windows, etc; just make sure you're using python 3.7 or 3.8)
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
- [ ] On-Message (and other on-anything gateway) capabilities (coming soon)
- [ ] Making phone calls, sending audio/video data thru those calls
- [ ] Everything

# list of all 121 functions (click thru these and github should show their location in discum.py) **slightly changed in v0.3.0, will update soon
```python
discum.Client(email="none", password="none", token="none", proxy_host=None, proxy_port=None, user_agent="random", log=True)
connectionTest(self)
snowflake_to_unixts(snowflake)
unixts_to_snowflake(unixts)
read(update=True)
getGuilds(update=True)
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
getAnalyticsToken(update=True)
getConnectedAccounts(update=True)
getConsents(update=True)
getExperiments(update=True)
getFriendSuggestionCount(update=True)
getGuildExperiments(update=True)
getNotOfflineFriends(update=True)
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
getUserGuildSettings(guildID=None,update=True)
getUserSettings(update=True)
getOptionsForUserSettings(update=True)
getGeoOrderedRtcRegions(update=True)
getCachedUsers(update=True)
getWebsocketVersion(update=True)
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
getGuildMember(guildID,userID)
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

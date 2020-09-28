# Wiki

## Quickstart:
#### Install:
```
git clone https://github.com/Merubokkusu/Discord-S.C.U.M.git
cd Discord-S.C.U.M
python3 setup.py install
```
#### Initiate client
```python
>>> import discum
>>> bot = discum.Client(email='email@email.com',password='password')
'Randomly generated user agent: Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_4 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) CriOS/32.0.1700.20 Mobile/10B350 Safari/8536.25'
 [+] (<discum.login.Login.Login->Connect) Post -> https://discord.com/api/v8/auth/login
 [+] (<discum.login.Login.Login->Connect) {"email": "email@email.com", "password": "passwrod", "undelete": false, "captcha_key": null, "login_source": null, "gift_code_sku_id": null}
 [+] (<discum.login.Login.Login->Connect) Response <- {"token": "420tokentokentokentoken.token.tokentokentokentokentoken", "user_settings": {"locale": "en-US", "theme": "dark"}}
'Retrieving Discord's build number...'
'Discord is currently on build number 68015'
```
## Commands
- [Read User Data](#read-user-data)
- [Messages](#Messages)
- [User Actions](#User-Actions)
- [Gateway Server](#Gateway-Server)
#### Read User Data:
\* this connects to discord's gateway server and returns your current session settings. It's recommended that you set update to False after you run a command since you can only connect so many times to the gateway until discord gets suspicious (maximum recommended connections per day is 1000)
```bot.read(update=True)```
```bot.getAnalyticsToken(update=True)```
```bot.getConnectedAccounts(update=True)```
```bot.getConsents(update=True)```
```bot.getExperiments(update=True)```
```bot.getFriendSuggestingCount(update=True)```
```bot.getGuildExperiments(update=True)```
```bot.getGuilds(update=True)```
```bot.getGuildIDs(update=True)```
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
```bot.getGuildVoiceStates(guildID,update=True)```
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
```bot.getGuildMembers(guildID,update=True)```
```bot.getGuildMemberIDs(guildID,update=True)```
```bot.getGuildMemberData(guildID,memberID,update=True)```
```bot.getNotes(update=True)```
```bot.getOnlineFriends(update=True)```
```bot.getDMs(update=True)```
```bot.getDMIDs(update=True)```
```bot.getDMData(DMID,update=True)```
```bot.getDMRecipients(DMID,update=True)```
```bot.getReadStates(update=True)```
```bot.getRelationships(update=True)```
| Relationship Type | description |
| ------ | ------ |
| 1 | friend |
| 2 | block |
| 3 | incoming friend request |
| 4 | outgoing friend request |
```bot.getRelationshipIDs(update=True)```
```bot.getRelationshipData(RelationshipID,update=True)```
```bot.getFriends(update=True)```
```bot.getFriendIDs(update=True)```
```bot.getBlocked(update=True)```
```bot.getBlockedIDs(update=True)```
```bot.getIncomingFriendRequests(update=True)```
```bot.getIncomingFriendRequestIDs(update=True)```
```bot.getOutgoingFriendRequests(update=True)```
```bot.getOutgoingFriendRequestIDs(update=True)```
```bot.getSessionID(update=True)```
```bot.getTutorial(update=True)```
```bot.getUserData(update=True)```
```bot.getUserGuildSettings(update=True,guildID=None)```
```bot.getUserSettings(update=True)```
```bot.getOptionsForUserSettings(update=True)```
```bot.getWebsocketVersion(update=True)```

#### Messages
##### get messages in a channel
```getRecentMessage(ChannelID,num=1,beforeDate=None)```
```python
bot.getRecentMessage("383003333751856129") #if beforeDate not given, then most recent message(s) will be returned
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
#### User Actions
##### send friend request
```requestFriend(userID)```
```python
bot.requestFriend(ID)
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
#### Gateway Server
```_Client__gateway_server.runIt(taskdata)```
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
the input consists of "send" and "receive" data:
```
{
  1: {
    "send": [{...}, {...}, {...}],
    "receive": [{...}]
  },
  2: {
    "send": [{...}],
    "receive": [{...}, {...}]
  }, ...
}
```
the "send" data is a list of what you send, op code and all.
the "receive" data is formatted like so:
```
{
  "key":(optional; type list of tuples of strings/ints),
  "keyvalue": (optional; type list of tuples of key&value)
}
```
and here's a closer look at the values in the "receive" data:
```
{
  "key": [("keys","in","nesting","order"),("keys2","in2","nesting2","order2"),...]
  "keyvalue": [(("keys","in","nesting","order"),value_to_check_for2),(("keys2","in2","nesting2","order2"),value_to_check_for2),...]
}
```
and to clear up any confusion, key looks for the existence of keys and keyvalue looks to see if a specific key has a specific value. Since you can check multiple keys and/or multiple key-value pairs per task, the possibilities are literally endless for what you can look for :)
simple example: here's the minimum amount of data a task can have (the command below simply connects to the gateway server and listens for messages from discord):
```python
bot._Client__gateway_server.runIt({
  1: {
    "send": [],
    "receive": []
  }
})
```

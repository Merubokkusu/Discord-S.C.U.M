# REST actions
If no parameters are specified then there are none.          
Unless otherwise specified, functions below return a [requests.Response object](https://docs.python-requests.org/en/latest/api/#requests.Response).     
__________
### Start
##### ```getBuildNumber```
```python
bot.getBuildNumber()
```
##### ```getSuperProperties```
```python
bot.getSuperProperties('Opera/8.17 (Windows NT 5.1; sl-SI) Presto/2.8.215 Version/11.00')
```
###### Parameters:
-   user_agent (str)
-   buildnum (Optional[int]) - discord's build number. Defaults to "request"
-   locale (Optional[str]) - only use this if you're logging in with email&pass
###### Returns:
[superproperties dictionary](https://luna.gitlab.io/discord-unofficial-docs/science.html#super-properties-object)

##### ```getXFingerprint```
```python
bot.getXFingerprint()
```
###### Returns:
xfingerprint string

##### ```login```
```python
bot.login('email@email.com', 'password')
```
###### Parameters:
- email (str)
- password (str)
- undelete (Optional[bool]) - recover an account that was disabled/deleted by a user. Defaults to False
- captcha (Optional[str]) - captcha key
- source (Optional) - unknown
- gift_code_sku_id (Optional) - unknown
- secret (Optional[str]) - 2FA secret
- code (Optional[str]) - 2FA TOTP (6-digit) code
###### Returns:
(login response object, xfingerprint string)

##### ```getGatewayUrl```
```python
bot.getGatewayUrl()
```

##### ```getDiscordStatus```
```python
bot.getDiscordStatus()
```
(status of Discord's servers)
##### ```getDetectables```
```python
bot.getDetectables()
```
##### ```getOauth2Tokens```
```python
bot.getOauth2Tokens()
```
##### ```getVersionStableHash```
```python
bot.getVersionStableHash()
```
__________
### User
| relationship type | description |
| ----------- | ----------- |
| 1 | friend |
| 2 | block |
| 3 | incoming friend request |
| 4 | outgoing friend request |

##### ```getRelationships```
```python
bot.getRelationships()
```

##### ```requestFriend```
\*_risky action_
```python
bot.requestFriend("222222222222222222")
bot.requestFriend("test#0000")
```
###### Parameters:
- user (str) - either id or username#discriminator

##### ```acceptFriend```
```python
bot.acceptFriend(ID, location)
```
###### Parameters:
- userID (str)
- location (Optional[str]) - "friends", "context menu", or "user profile". Defaults to "friends"

##### ```removeRelationship```
```python
bot.removeRelationship(ID, location)
```
###### Parameters:
- userID (str)
- location (Optional[str]) - "friends", "context menu", or "user profile". Defaults to "context menu"

##### ```blockUser```
```python
bot.blockUser(ID, location)
```
###### Parameters:
- userID (str)
- location (Optional[str]) - "friends", "context menu", or "user profile". Defaults to "context menu"

##### ```getProfile```
```python
bot.getProfile('222222222222222222')
```
###### Parameters:
- userID (str)
- with_mutual_guilds (Optional[bool/None]) - get mutual guilds. Defaults to True

##### ```info```
```python
bot.info(True)
```
###### Parameters:
- with\_analytics\_token (Optional[bool/None]) - this token is passed in the body of science/analytics requests. Defaults to None

##### ```getUserAffinities```
```python
bot.getUserAffinities()
```
##### ```getGuildAffinities```
```python
bot.getGuildAffinities()
```
##### ```getMentions```
```python
bot.getMentions()
```
###### Parameters:
- limit (Optional[int]) - number of mentions to fetch. Defaults to 25
- roleMentions (Optional[bool]) - defaults to True
- everyoneMentions (Optional[bool]) - defaults to True

##### ```removeMentionFromInbox```
```python
bot.removeMentionFromInbox('222222222222222222')
```
###### Parameters:
- message ID (str)

##### ```getMyStickers```
```python
bot.getMyStickers()
```
##### ```getNotes```
```python
bot.getNotes('222222222222222222')
```
###### Parameters:
- user ID (str)

##### ```getRTCregions```
```python
bot.getRTCregions()
```

##### ```setUsername```
\*bot.\_Client\_\_user\_password needs to be set before running this
```python
bot.setUsername('helloworld')
```
###### Parameters:
- new username (str)

##### ```setEmail```
\*bot.\_Client\_\_user\_password needs to be set before running this
```python
bot.setEmail('helloworld@example.com')
```
###### Parameters:
- new email (str)

##### ```setPassword```
\*bot.\_Client\_\_user\_password needs to be set before running this
```python
bot.setPassword('verysecurepass')
```
###### Parameters:
- new password (str)

##### ```setDiscriminator```
\*bot.\_Client\_\_user\_password needs to be set before running this
```python
bot.setDiscriminator('0001')
```
###### Parameters:
- new discriminator (str)

##### ```setAvatar```
\*_risky action_
```python
bot.setAvatar('./catpics/001.png')
```
###### Parameters:
- image path (str)

##### ```setAboutMe```
currently, you need to be in the beta testing program for this to work
```python
bot.setAboutMe('hello world')
```
###### Parameters:
- bio (str)

##### ```setBanner```
currently, you need to be in the beta testing program with nitro for this to work
```python
bot.setBanner('./catpics/001.png')
```
###### Parameters:
- image path (str)

##### ```getTOTPurl```
```python
bot.getTOTPurl(secret = bot._Client__totp_secret)
```
###### Parameters:
- 2FA secret (str)

##### ```calculateTOTPcode```
```python
bot.calculateTOTPcode(secret = bot._Client__totp_secret)
```
###### Parameters:
- 2FA secret (str)

##### ```enable2FA```
automatically updates your token
```python
bot.enable2FA()
```

##### ```disable2FA```
automatically updates your token
```python
bot.disable2FA()
```
###### Parameters:
- code (Optional[str]) - TOTP code. Defaults to "calculate"
- clearSecretAfter (Optional[bool]) - clear TOTP secret from memory after running. Defaults to False (to prevent accidental account loss if TOTP code fails)

##### ```getBackupCodes```
\*bot.\_Client\_\_user\_password needs to be set before running this
```python
bot.getBackupCodes()
```
###### Parameters:
- regenerate (Optional[bool]) - defaults to False

##### ```disableAccount```
```python
bot.disableAccount("verysecurepass")
```
###### Parameters:
- password (str)

##### ```deleteAccount```
```python
bot.deleteAccount("verysecurepass")
```
###### Parameters:
- password (str)

##### ```setDMscanLvl```
```python
bot.setDMscanLvl(0)
```
###### Parameters:
- level (Optional[int]) - can be 0, 1, or 2. defaults to 1

##### ```allowDMsFromServerMembers```
```python
bot.allowDMsFromServerMembers()
```
###### Parameters:
- allow (Optional[bool]) - defaults to True
- disallowedGuildIDs (Optional[list])

##### ```allowFriendRequestsFrom```
```python
bot.allowFriendRequestsFrom(["mutual_friends"])
```
###### Parameters:
- types (Optional[list]) - defaults to ["everyone", "mutual\_friends", "mutual\_guilds"]

##### ```analyticsConsent```
```python
bot.analyticsConsent(grant="usage_statistics", revoke="personalization")
```
###### Parameters:
- grant (Optional[list]) - defaults to []
- revoke (Optional[list]) - defaults to []

##### ```allowScreenReaderTracking```
```python
bot.allowScreenReaderTracking()
```

###### Parameters:
- allow (Optional[bool]) - defaults to True

##### ```requestMyData```
```python
bot.requestMyData()
```

##### ```getConnectedAccounts```
```python
bot.getConnectedAccounts()
```

##### ```getConnectionUrl```
```python
bot.getConnectionUrl("reddit")
```

###### Parameters:
- accountType (str) - "twitch", "youtube", "battlenet", "steam", "reddit", "facebook", "twitter", "spotify", "xbox", or "github"

##### ```enableConnectionDisplayOnProfile```
```python
bot.enableConnectionDisplayOnProfile("reddit", "skjdnfksjfkdjfskjdnksdjfhksdjfksjdksjnfd")
```

###### Parameters:
- accountType (str) - "twitch", "youtube", "battlenet", "steam", "reddit", "facebook", "twitter", "spotify", "xbox", or "github"
- accountUsername (str)
- enable (Optional[str]) - defaults to True

##### ```enableConnectionDisplayOnStatus```
```python
bot.enableConnectionDisplayOnStatus("reddit", "skjdnfksjfkdjfskjdnksdjfhksdjfksjdksjnfd")
```

###### Parameters:
- accountType (str) - "twitch", "youtube", "battlenet", "steam", "reddit", "facebook", "twitter", "spotify", "xbox", or "github"
- accountUsername (str)
- enable (Optional[str]) - defaults to True

##### ```removeConnection```
```python
bot.removeConnection("reddit", "skjdnfksjfkdjfskjdnksdjfhksdjfksjdksjnfd")
```

###### Parameters:
- accountType (str) - "twitch", "youtube", "battlenet", "steam", "reddit", "facebook", "twitter", "spotify", "xbox", or "github"
- accountUsername (str)

##### ```getBillingHistory```
```python
bot.getBillingHistory()
```
###### Parameters:
- limit (Optional[int]) - defaults to 20

##### ```getPaymentSources```
```python
bot.getPaymentSources()
```
##### ```getBillingSubscriptions```
```python
bot.getBillingSubscriptions()
```
##### ```getStripeClientSecret```
```python
bot.getStripeClientSecret()
```

##### ```setTheme```
```python
bot.setTheme("dark")
```
###### Parameters:
- theme (str) - light or dark

##### ```setMessageDisplay```
```python
bot.setMessageDisplay("cozy")
```
###### Parameters:
- CozyOrCompact (str) - cozy or compact

##### ```enableGifAutoPlay```
```python
bot.enableGifAutoPlay()
```
###### Parameters:
- enable (Optional[bool]) - defaults to True

##### ```enableAnimatedEmoji```
```python
bot.enableAnimatedEmoji()
```
###### Parameters:
- enable (Optional[bool]) - defaults to True

##### ```setStickerAnimation```
```python
bot.setStickerAnimation("interaction")
```
###### Parameters:
- setting (str) - "always", "interaction", or "never"

##### ```enableTTS```
```python
bot.enableTTS()
```
###### Parameters:
- enable (Optional[bool]) - defaults to True

##### ```enableLinkedImageDisplay```
```python
bot.enableLinkedImageDisplay()
```
###### Parameters:
- enable (Optional[bool]) - defaults to True

##### ```enableImageDisplay```
```python
bot.enableImageDisplay()
```
###### Parameters:
- enable (Optional[bool]) - defaults to True

##### ```enableLinkPreview```
```python
bot.enableLinkPreview()
```
###### Parameters:
- enable (Optional[bool]) - defaults to True

##### ```enableReactionRendering```
```python
bot.enableReactionRendering()
```
###### Parameters:
- enable (Optional[bool]) - defaults to True

##### ```enableEmoticonConversion```
```python
bot.enableEmoticonConversion()
```
###### Parameters:
- enable (Optional[bool]) - defaults to True

##### ```setAFKtimeout```
```python
bot.setAFKtimeout(500)
```
###### Parameters:
- timeout_seconds (int)

##### ```setLocale```
```python
bot.setLocale("en-US")
```
###### Parameters:
- locale (str)

##### ```enableDevMode```
```python
bot.enableDevMode()
```
###### Parameters:
- enable (Optional[bool]) - defaults to True

##### ```activateApplicationTestMode```
```python
bot.activateApplicationTestMode('10101010101010')
```
###### Parameters:
- applicationID (str)

##### ```getApplicationData```
```python
bot.getApplicationData('10101010101010')
```
###### Parameters:
- applicationID (str)
- with\_guild (Optional[str]) - defaults to False

##### ```enableActivityDisplay```
```python
bot.enableActivityDisplay()
```
###### Parameters:
- enable (Optional[bool]) - defaults to True

##### ```setHypesquad```
```python
bot.setHypesquad("bravery")
bot.setHypesquad("brilliance")
bot.setHypesquad("balance")
```
###### Parameters:
- house (str) - bravery, brilliance, or balance

##### ```leaveHypesquad```
```python
bot.leaveHypesquad()
```

##### ```getBuildOverrides```
```python
bot.getBuildOverrides()
```

##### ```enableSourceMaps```
doesn't work if you're not a dev at discord
```python
bot.enableSourceMaps()
```

###### Parameters:
- enable (Optional[bool]) - defaults to True

##### ```suppressEveryonePings```
```python
bot.suppressEveryonePings('0000000000000000000')
```

###### Parameters:
- guildID (str)
- suppress (Optional[bool]) - defaults to True

##### ```suppressRoleMentions```
```python
bot.suppressRoleMentions('0000000000000000000')
```

###### Parameters:
- guildID (str)
- suppress (Optional[bool]) - defaults to True

##### ```enableMobilePushNotifications```
```python
bot.enableMobilePushNotifications('0000000000000000000')
```

###### Parameters:
- guildID (str)
- enable (Optional[bool]) - defaults to True

##### ```setChannelNotificationOverrides```
```python
bot.setChannelNotificationOverrides('0000000000000000000', [('1111111111111', 'only mentions', False), ('2222222222222', 'nothing', True)])
```

###### Parameters:
- guildID (str)
- overrides (list) - list of tuples containing data about channel notification overrides. Each tuple looks like ('channelID', 'msg notifications type', 'mute'). 'msg notifications type' is either "all messages" or "only mentions" or "nothing". 'mute' is a boolean. If instead you'd like to input the raw overrides dictionary, you can do that instead.

##### ```setMessageNotifications```
```python
bot.setMessageNotifications('0000000000000000000', 'all messages')
```

###### Parameters:
- guildID (str)
- notifications (str) - either "all messages" or "only mentions" or "nothing"

##### ```muteGuild```
```python
bot.muteGuild('0000000000000000000', duration=15)
```

###### Parameters:
- guildID (str)
- mute (Optional[bool]) - defaults to True
- duration (Optional[int]) - duration of mute in minutes

##### ```muteDM```
```python
bot.muteDM('0000000000000000000', duration=900)
```

###### Parameters:
- DMID (str)
- mute (Optional[bool]) - defaults to True
- duration (Optional[int]) - duration of mute in minutes

##### ```logout```
```python
bot.logout()
```
###### Parameters:
- provider (Optional) - unknown
- voip_provider (Optional)
__________
### Science/Analytics
"Science", aka Discord's analytics/tracking. "Discord argues that they need to collect the data in the case the User allows the usage of the data later on. Which [...] is complete bullshit. Have a good day." ([source](https://luna.gitlab.io/discord-unofficial-docs/science.html#tracking))

##### ```science```
```python
bot.science([{}])
```
###### Parameters:
- events (list) - a list of [science events](https://luna.gitlab.io/discord-unofficial-docs/science.html). Minimal input is [{}] which defaults to a keyboard\_mode\_toggled event.

##### ```calculateClientUUID```
[more info](https://docs.google.com/document/d/1b5aDx7S1iLHoeb6B56izZakbXItA84gUjFzK-0OBwy0/edit?usp=sharing)
```python
bot.calculateClientUUID()
```
###### Parameters:
- eventNum (Optional[int]) - client uuid calculation is sequencial. By default, eventNum starts at 0.
- userID (optional[str]) - defaults to your userID. If you're not logged in, the current discord snowflake is used instead.
- increment (optional[bool]) - toggle sequencial aspect of client uuid calculation. Defaults to True
###### Returns:
client UUID string

##### ```refreshClientUUID```
```python
bot.refreshClientUUID()
```
###### Parameters:
- resetEventNum (Optional[bool]) - event number is one of the variables that goes into calculating client UUID. Defaults to True
###### Returns:
client UUID string

##### ```parseClientUUID```
\*userID and creationTime calculations are guesses
```python
bot.parseClientUUID('AAASXwTHGwfnejRw+qeUEncBAAAAAAAA')
```
###### Parameters:
- client_uuid (str)
###### Returns:
UUIDdata dict (keys = ["userID", "randomPrefix", "creationTime", "eventNum"])
__________
### Guild
##### ```getInfoFromInviteCode```
```python
bot.getInfoFromInviteCode('minecraft')
```
###### Parameters:
- inviteCode (str) - just the invite code, NOT the entire link
- with_counts (Optional[bool/None]) - get approx online and member counts. Defaults to True
- with_expiration (Optional[bool/None]) - get invite expiration. Defaults to True
- fromJoinGuildNav (Optional[bool]) - if joining guild from within guild app. Defaults to False

##### ```joinGuild```
\*_risky action_
```python
bot.joinGuild('1a1a1')
```
###### Parameters:
- inviteCode (str) - just the invite code, NOT the entire link
- location (Optional[str]) - "accept invite page" or "join guild". Defaults to "accept invite page"
- wait (Optional[int]) - this function uses 2 endpoints: getInfoFromInviteCode and a raw join guild endpoint; wait specifies the time to wait inbetween these 2 requests. Defaults to 0. 

##### ```leaveGuild```
```python
bot.leaveGuild('guildID00000000000')
```
###### Parameters:
- guild ID (str)

##### ```createInvite```
```python
bot.createInvite('channelID00000000000')
```
###### Parameters:
- channel ID (str)
- max\_age\_seconds (Optional[int/bool]) - how long invite should last. Defaults to False
- max\_uses (Optional[int/bool]) - how many invite uses. Defaults to False
- grantTempMembership (Optional[bool]) - defaults to False
- checkInvite (Optional[str]) - invite code to check. Defaults to ""
- targetType (Optional[str]) - unknown. Defaults to ""

##### ```getGuilds```
```python
bot.getGuilds()
```
###### Parameters:
- with_counts (bool/Nonetype) - get approx online and member counts. Defaults to True

##### ```createGuild```
```python
bot.createGuild('hello world', icon='cat.jpg')
```
###### Parameters:
- name (str)
- icon (Optional[str]) - image path
- channels (Optional[list]) - list of channels (https://discord.com/developers/docs/resources/channel#channel-object)
- systemChannelID (Optional[str])
- template (Optional[str]) - defaults to "2TffvPucqHkN"


##### ```deleteGuild```
```python
bot.deleteGuild('guildID00000000000')
```
###### Parameters:
- guildID (str)

##### ```kick```
```python
bot.kick('guildID00000000000','userID11111111111','weeeee')
bot.kick('guildID00000000000','userID11111111111')
```
###### Parameters:
- guildID (str)
- userID (str)
- reason (Optional[str]) - defaults to ""

##### ```ban```
```python
bot.ban('guildID00000000000','userID11111111111',7,'weeeee')
```
###### Parameters:
- guildID (str)
- userID (str)
- deleteMessagesDays (Optional[int]) - how many days of msgs to delete from user. Defaults to 0
- reason (Optional[str]) - defaults to ""

##### ```revokeBan```
```python
bot.revokeBan('guildID00000000000','userID11111111111')
```
###### Parameters:
- guildID (str)
- userID (str)

##### ```getRoleMemberCounts```
```python
bot.getRoleMemberCounts('guildID00000000000')
```

###### Parameters:
- guildID (str)

##### ```getMemberVerificationData```
```python
memberVerificationData = bot.getMemberVerificationData("guildID000000000000").json()
```
###### Parameters:
- guildID (str)
- with_guild (Optional[bool]) - defaults to False
- invite_code (Optional[str])

##### ```agreeGuildRules```
```python
bot.agreeGuildRules("guildID000000000000", memberVerificationData["form_fields"], memberVerificationData["version"])
```
###### Parameters:
- guildID (str)
- form_fields (list) - from getMemberVerificationData(...)
- version (str) - from getMemberVerificationData(...). Defaults to "2021-01-05T01:44:32.163000+00:00"

__________
### Messages
##### ```createDM```
\*_risky action_
```python
newDM = bot.createDM(["userID000000000000"]).json()["id"] 
bot.sendMessage(newDM, "hello")
```
###### Parameters:
- recipients (list) - list of user ID strings

##### ```getMessages```
```python
bot.getMessages("channelID0000000000")
```
###### Parameters:
- ChannelID (str)
- num (Optional[int]) - number of messages to fetch (0<=num<=100). Defaults to 1
- beforeDate (Optional[str]) - discord snowflake
- aroundMessage (Optional[str]) - message ID

##### ```getMessage```
```python
bot.getMessage('channelID0000000000','msgID000000000000')
```
###### Parameters:
- channelID (str)
- messageID (str)

##### ```greet```
```python
bot.greet('channelID0000000000', ["749054660769218631"])
```
###### Parameters:
- channelID (str)
- sticker_ids (list)

##### ```Embedder```
```python
embed = bot.Embedder()
embed.title("This is a test")
embed.image('https://cdn.dribbble.com/users/189524/screenshots/2105870/04-example_800x600_v4.gif')
embed.fields('Hello!',':yum:')
embed.fields(':smile:','Testing :)')
embed.author('Tester')
embed.color(15158332) # Colors must be integer
bot.sendMessage("383006063751856129","", embed=embed.read())
```

##### ```sendMessage```
```python
bot.sendMessage("383003333751856129","Hello You :)")
```
###### Parameters:
- channelID (str)
- message (str)
    * \*\*bold\*\*
    * \*italicized\*
    * \~\~strikethrough\~\~
    * \>quoted
    * \`code\`
    * \|\|spoiler\|\|
- nonce (Optional[str]) - current discord snowflake. By default, this is calculated
- tts (Optional[bool]) - text-to-speech. Defaults to False
- embed (Optional[dict]) See [section on sending embeds](#Embedder) above. Defaults to None
- message\_reference (Optional[dict]) - ```{"channel_id":channelID,"message_id":messageID}``` is the usual format. Defaults to None
- allowed\_mentions (Optional[dict]) - ```{"parse":["users","roles","everyone"],"replied_user":False}``` is the usual format. Defaults to None
- sticker\_ids (Optional[list]) - defaults to None

##### ```sendFile```
```python
bot.sendFile("channelID0000000","https://thiscatdoesnotexist.com",True)
```
###### Parameters:
- channelID (str)
- filelocation (str) - either local file or url
    * spoiler images: rename image to SPOILER_image
- isurl (Optional[bool]) - defaults to False
- message (Optional[str]) - defaults to ""
- tts (Optional[str]) - text-to-speech. Defaults to False
- message_reference (Optional[dict]) - see parameters of [send message](#sendMessage) for details
- sticker_ids (Optional[list]) - defaults to None

##### ```reply```
```python
bot.reply('222222222222222222','000000000000000000', 'this is a reply', sticker_ids=['444444444444444444'], file="https://thiscatdoesnotexist.com/", isurl=True)
```
###### Parameters:
- channelID (str)
- messageID (str)
- message (str)
- nonce (Optional[str]) - discord snowflake. By default, this is calculated
- tts (Optional[bool]) - text-to-speech. Defaults to False
- embed (Optional[dict]) See [section on sending embeds](#Embedder) above. Defaults to None
- allowed\_mentions (Optional[dict]) - see parameters of [send message](#sendMessage) for details
- sticker_ids (Optional[list]) - defaults to None
- filelocation (str) - either local file or url
    * spoiler images: rename image to SPOILER_image
- isurl (Optional[bool]) - defaults to False

##### ```searchMessages```
```python
bot.searchMessages("guildID000000000",textSearch="hello")
```
###### Parameters:
- guildID (str)
- channelID (Optional[str/list]) - channel ID string(s)
- authorID (Optional[str/list]) - author ID string(s)
- authorType (Optional[str/list]) - author type(s): "user", "bot", and/or "webhook"
- mentionsUserID (Optional[str/list]) - user ID string(s)
- has (Optional[str/list]) - media type string(s): "link", "embed", "file", "video", "image", and/or "sound"
- linkHostname (Optional[str/list]) - like "http://example.com" or "example.com"
- embedProvider (Optional[str/list]) - the provider_name returned by https://oembed.com/, for example, "Flickr"
- embedType (Optional[str/list]) - the type returned by https://oembed.com/, for example, "photo"
- attachmentExtension (Optional[str/list])
- attachmentFilename (Optional[str/list])
- mentionsEveryone (Optional[bool]) - return msgs that actually mention everyone (only if said user had perms to mention everyone)
- includeNsfw (Optional[bool])
- afterDate (Optional[str]) - discord snowflake string (highest msg id)
- beforeDate (Optional[str]) - discord snowflake string (highest msg id)
- textSearch (Optional[str])
- afterNumResults (Optional[int]) - multiples of 25
- limit (Optional[int]) - how many results to show

##### ```filterSearchResults```
```python
searchResponse = bot.searchMessages("guildID000000000",textSearch="hello")
results = bot.filterSearchResults(searchResponse)
```
###### Parameters:
- searchResponse (requests.Response object)
###### Returns:
- list of targeted results

##### ```typingAction```
this lasts for ~10 seconds
```python
bot.typingAction("channelID0000000")
```
###### Parameters:
- channelID (str)

##### ```editMessage```
```python
bot.editMessage("channelID0000000","msgID000000000","hi")
```
###### Parameters:
- channelID (str)
- messageID (str)
- newMessage (str)

##### ```deleteMessage```
```python
bot.deleteMessage("channelID0000000","msgID000000000")
```
###### Parameters:
- channelID (str)
- messageID (str)

##### ```pinMessage```
```python
bot.pinMessage("channelID0000000","msgID000000000")
```
###### Parameters:
- channelID (str)
- messageID (str)

##### ```unPinMessage```
```python
bot.unPinMessage("channelID0000000","msgID000000000")
```
###### Parameters:
- channelID (str)
- messageID (str)

##### ```getPins```
```python
bot.getPins("channelID0000000")
```
###### Parameters:
- channelID (str)

##### ```addReaction```
```python
bot.addReaction("channelID0000000","msgID000000000","👻")
bot.addReaction("channelID0000000","msgID000000000","wowee:720507026014450205")
```
###### Parameters:
- channelID (str)
- messageID (str)
- emoji or emojiName:emojiID (str)

##### ```removeReaction```
```python
bot.removeReaction("channelID0000000","msgID000000000","👻")
bot.removeReaction("channelID0000000","msgID000000000","wowee:720507026014450205")
```
###### Parameters:
- channelID (str)
- messageID (str)
- emoji or emojiName:emojiID (str)

##### ```ackMessage```
```python
bot.ackMessage("channelID0000000","msgID000000000")
```
###### Parameters:
- channelID (str)
- messageID (str)
- ackToken (Optional[str])

##### ```unAckMessage```
```python
bot.unAckMessage("channelID0000000","msgID000000000",250)
```
###### Parameters:
- channelID (str)
- messageID (str)
- numMentions (Optional[str]) - how many mentions to show in discord tab. Defaults to 0

##### ```bulkAck```
```python
bot.bulkAck([{"channelID0000000":"msgID000000000"},{"channelID111111":"msgID11111111"}])
```
###### Parameters:
- data (list) - list of dictionaries [{channelID:messageID}, etc]

##### ```getTrendingGifs```
```python
bot.getTrendingGifs()
```
###### Parameters:
- provider (Optional[str]) - defaults to "tenor"
- locale (Optional[str]) - defaults to "en-US"
- media\_format (Optional[str]) - defaults to "mp4"
__________
### Stickers
##### ```getStickers```
```python
bot.getStickers()
```
###### Parameters:
- directoryID (Optional[str]) - defaults to "758482250722574376"
- store_listings (Optional[bool]) - defaults to False
- locale (Optional[str]) - defaults to "en-US"

##### ```getStickerFile```
```python
bot.getStickerFile("749052944682582036", "5bc6cc8f8002e733e612ef548e7cbe0c")
```
###### Parameters:
- stickerID (str) - can be found using getStickers
- stickerAsset (str) - can be found using getStickers

##### ```getStickerJson```
```python
bot.getStickerJson("749052944682582036", "5bc6cc8f8002e733e612ef548e7cbe0c")
```
###### Parameters:
- stickerID (str) - can be found using getStickers
- stickerAsset (str) - can be found using getStickers

##### ```getStickerPack```
```python
bot.stickerPackID('749043879713701898')
```
###### Parameters:
- stickerPackID (str) - can be found using getStickers

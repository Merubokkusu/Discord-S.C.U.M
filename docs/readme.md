# Discum
A simple, easy to use, non-restrictive Discord API Wrapper for Selfbots/Userbots written in Python.        
![version](https://img.shields.io/badge/latest%20version-1.0.0-blue) [![python versions](https://img.shields.io/badge/python-2.7%20%7C%203.5%20%7C%203.6%20%7C%203.7%20%7C%203.8-blue)](https://github.com/Merubokkusu/Discord-S.C.U.M)
__________
# Table of Contents
- [Using discum](https://github.com/Merubokkusu/Discord-S.C.U.M/blob/master/docs/using.md) (make selfbots and userbots)
  - [fetching guild members](https://github.com/Merubokkusu/Discord-S.C.U.M/blob/master/docs/fetchingGuildMembers.md)
- [Extending discum](https://github.com/Merubokkusu/Discord-S.C.U.M/blob/master/docs/extending.md) (add discord API wraps)
- [Reading discum](https://github.com/Merubokkusu/Discord-S.C.U.M/blob/master/docs/reading.md) (structure of discum)
___________
# Overview:

### 292 functions:      
```
# client initialization
discum.Client(email="", password="", secret="", code="", token="", proxy_host=None, proxy_port=None, user_agent="random", log=True)
```

```
# HTTP API
connectionTest()
snowflake_to_unixts(snowflake)
unixts_to_snowflake(unixts)
login(email, password, undelete=False, captcha=None, source=None, gift_code_sku_id=None, secret="", code="")
getXFingerprint()
getBuildNumber()
getSuperProperties(user_agent, buildnum="request")
getGatewayUrl()
getDiscordStatus()
getDetectables()
getOauth2Tokens()
getVersionStableHash(underscore=None)
createDM(recipients)
getMessages(channelID,num=1,beforeDate=None,aroundMessage=None)
getMessage(channelID, messageID)
sendMessage(channelID, message, nonce="calculate", tts=False, embed=None, message_reference=None, allowed_mentions=None, sticker_ids=None)
sendFile(channelID,filelocation,isurl=False,message="", tts=False, message_reference=None, sticker_ids=None)
reply(channelID, messageID, message, nonce="calculate", tts=False, embed=None, allowed_mentions={"parse":["users","roles","everyone"],"replied_user":False}, sticker_ids=None, file=None, isurl=False)
searchMessages(guildID,channelID=None,userID=None,mentionsUserID=None,has=None,beforeDate=None,afterDate=None,textSearch=None,afterNumResults=None)
filterSearchResults(searchResponse)
typingAction(channelID)
deleteMessage(channelID,messageID)
editMessage(channelID,messageID,newMessage)
pinMessage(channelID,messageID)
unPinMessage(channelID,messageID)
getPins(channelID)
addReaction(channelID,messageID,emoji)
removeReaction(channelID,messageID,emoji)
ackMessage(channelID,messageID,ackToken=None)
unAckMessage(channelID,messageID,numMentions=0)
bulkAck(data)
getTrendingGifs(provider="tenor", locale="en-US", media_format="mp4")
getStickers(directoryID="758482250722574376", store_listings=False, locale="en-US")
getStickerFile(stickerID, stickerAsset)
getStickerJson(stickerID, stickerAsset)
getStickerPack(stickerPackID)
requestFriend(user)
acceptFriend(userID)
removeRelationship(userID)
blockUser(userID)
setStatus(status)
setAvatar(imagePath)
setUsername(username)
setEmail(email)
setPassword(new_password)
setDiscriminator(discriminator)
getProfile(userID)
info(with_analytics_token=None)
getUserAffinities()
getGuildAffinities()
getMentions(limit=25, roleMentions=True, everyoneMentions=True)
removeMentionFromInbox(messageID)
setHypesquad(house)
leaveHypesquad()
setLocale(locale)
calculateTOTPcode(secret="default")
getTOTPurl(secret): #use this to store your totp secret/qr pic; btw url format is otpauth://totp/Discord
enable2FA()
disable2FA(code="calculate", clearSecretAfter=False)
getRTCregions()
setAFKtimeout(timeout_seconds)
setTheme(theme)
setMessageDisplay(CozyOrCompact)
enableDevMode(enable)
activateApplicationTestMode(applicationID)
getApplicationData(applicationID, with_guild=False)
getBackupCodes(regenerate=False)
enableInlineMedia(enable)
enableLargeImagePreview(enable)
enableGifAutoPlay(enable)
enableLinkPreview(enable)
enableReactionRendering(enable)
enableAnimatedEmoji(enable)
enableEmoticonConversion(enable)
setStickerAnimation(setting)
enableTTS(enable)
getBillingHistory(limit=20)
getPaymentSources()
getBillingSubscriptions()
getStripeClientSecret()
logout(provider=None, voip_provider=None)
getInfoFromInviteCode(inviteCode)
joinGuild(inviteCode)
kick(guildID,userID,reason="")
ban(guildID,userID,deleteMessagesDays=0,reason="")
getGuildMember(guildID,userID)
getMemberVerificationData(guildID, with_guild=False, invite_code=None)
agreeGuildRules(guildID, form_fields, version="2021-01-05T01:44:32.163000+00:00")
science(events)
calculateClientUUID(eventNum="default", userID="default", increment=True)
refreshClientUUID(resetEventNum=True)
parseClientUUID(client_uuid)
```

```
# Gateway API
bot.gateway.command()
bot.gateway.removeCommand(function)
bot.gateway.clearCommands()
bot.gateway.run(auto_reconnect=True)
bot.gateway.send(data)
bot.gateway.close()
bot.gateway.resetSession()
bot.gateway.session.read()
bot.gateway.session.user
bot.gateway.session.guilds
bot.gateway.session.guildIDs
bot.gateway.session.positions #your roles in each guild. 
bot.gateway.session.guild(guildID).data
bot.gateway.session.guild(guildID).unavailable
bot.gateway.session.guild(guildID).setData
bot.gateway.session.guild(guildID).modify
bot.gateway.session.guild(guildID).hasMembers
bot.gateway.session.guild(guildID).members
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
bot.gateway.session.guild(guildID).notOfflineCachedMembers #cached members, so, essentially, useless
bot.gateway.session.guild(guildID).notOfflineCachedMemberIDs #cached members, so, essentially, useless
bot.gateway.session.guild(guildID).notOfflineCachedMemberData(userID) #cached members, so, essentially, useless
bot.gateway.session.guild(guildID).mergedPresences #these are also useless, but theyre in the api so gotta wrap them
bot.gateway.session.guild(guildID).mergedPresenceIDs #useless
bot.gateway.session.guild(guildID).mergedPresenceData(userID) #useless
bot.gateway.session.guild(guildID).position #your roles in a specific guild
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
bot.gateway.session.relationship(userID).data
bot.gateway.session.relationship(userID).friendMergedPresenceData
bot.gateway.session.DMs
bot.gateway.session.DMIDs
bot.gateway.session.DM(DMID).data
bot.gateway.session.DM(DMID).recipients
bot.gateway.session.userGuildSettings
bot.gateway.session.userGuildSetting(guildID).data
bot.gateway.session.userSettings
bot.gateway.session.optionsForUserSettings
bot.gateway.session.mergedPresences
bot.gateway.session.analyticsToken
bot.gateway.session.connectedAccounts
bot.gateway.session.consents
bot.gateway.session.experiments
bot.gateway.session.friendSuggestionCount
bot.gateway.session.guildExperiments
bot.gateway.session.readStates
bot.gateway.session.geoOrderedRtcRegions
bot.gateway.session.cachedUsers
bot.gateway.session.tutorial
bot.gateway.session.mergedPresences #useless

## Event checking
resp.event.achievement_updated
resp.event.activity
resp.event.activity_join_request
resp.event.all_message_reactions_removed
resp.event.ban_added
resp.event.ban_removed
resp.event.braintree
resp.event.bulk_messages_deleted
resp.event.call
resp.event.call_deleted
resp.event.call_updated
resp.event.channel
resp.event.channel_deleted
resp.event.channel_read_state_updated
resp.event.channel_updated
resp.event.connections_updated
resp.event.emojis_updated
resp.event.entitlement
resp.event.entitlement_deleted
resp.event.entitlement_updated
resp.event.feed_settings_updated
resp.event.friend_suggestion
resp.event.friend_suggestion_deleted
resp.event.gift_code_updated
resp.event.guild
resp.event.guild_application_commands_updated
resp.event.guild_deleted
resp.event.guild_integrations_updated
resp.event.guild_member_chunk
resp.event.guild_member_list
resp.event.guild_member_updated
resp.event.guild_updated
resp.event.invite
resp.event.invite_deleted
resp.event.library_app_updated
resp.event.lobby
resp.event.lobby_deleted
resp.event.lobby_member_connected
resp.event.lobby_member_disconnected
resp.event.lobby_member_updated
resp.event.lobby_message
resp.event.lobby_updated
resp.event.lobby_voice_server_update
resp.event.lobby_voice_state_update
resp.event.message
resp.event.message_ack
resp.event.message_deleted
resp.event.message_reaction_emoji_removed
resp.event.message_updated
resp.event.note_updated
resp.event.oauth2_token_removed
resp.event.payment_sources_updated
resp.event.payments_updated
resp.event.pins_ack
resp.event.pins_updated
resp.event.presence_replaced
resp.event.presence_updated
resp.event.reaction_added
resp.event.reaction_removed
resp.event.ready
resp.event.ready_supplemental
resp.event.recent_mention_deleted
resp.event.recipient_added
resp.event.recipient_removed
resp.event.relationship_added
resp.event.relationship_removed
resp.event.required_action_updated
resp.event.response
resp.event.role
resp.event.role_deleted
resp.event.role_updated
resp.event.session_replaced
resp.event.settings_updated
resp.event.stickers_updated
resp.event.stream
resp.event.stream_deleted
resp.event.stream_server_updated
resp.event.stream_updated
resp.event.subscriptions_updated
resp.event.typing
resp.event.user_guild_settings_updated
resp.event.user_premium_guild_sub_slot
resp.event.user_premium_guild_sub_slot_updated
resp.event.user_updated
resp.event.voice_server_updated
resp.event.voice_state_updated
resp.event.webhooks_updated

## other functions
resp.parsed.auto()
bot.gateway.fetchMembers(guild_id, channel_id, method="overlap", keep=[], considerUpdates=True, reset=True, wait=None, priority=0)
bot.gateway.finishedMemberFetching(guild_id)
bot.gateway.request.lazyGuild(guild_id, channel_ranges, typing=None, threads=None, activities=None, members=None)
bot.gateway.request.searchGuildMembers(guild_ids, query, limit=10, presences=True)
resp.parsed.guild_member_list_update()
resp.parsed.message_create()
bot.gateway.request.DMchannel(channel_id)
bot.gateway.request.call(channelID, guildID=None, mute=False, deaf=False, video=False)
bot.gateway.request.endCall()
```

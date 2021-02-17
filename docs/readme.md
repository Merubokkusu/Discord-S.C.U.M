# Discum
A simple, easy to use, non-restrictive Discord API Wrapper for Selfbots/Userbots written in Python.        
![version](https://img.shields.io/badge/latest%20version-1.1.0-blue) [![python versions](https://img.shields.io/badge/python-2.7%20%7C%203.5%20%7C%203.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-blue)](https://github.com/Merubokkusu/Discord-S.C.U.M)
__________
# Table of Contents
- [Using discum](https://github.com/Merubokkusu/Discord-S.C.U.M/blob/master/docs/using.md) (make selfbots and userbots)
  - [fetching guild members](https://github.com/Merubokkusu/Discord-S.C.U.M/blob/master/docs/fetchingGuildMembers.md)
- [Extending discum](https://github.com/Merubokkusu/Discord-S.C.U.M/blob/master/docs/extending.md) (add discord API wraps)
- [Reading discum](https://github.com/Merubokkusu/Discord-S.C.U.M/blob/master/docs/reading.md) (structure of discum)
___________
## Some quick tips:
Note, here's a list of functions you should tread carefully when using if you don't want to get your account disabled:        
- bot.createDM
- bot.requestFriend
- bot.joinGuild
___________
# Overview:

### 296 functions:      
```
# client initialization
discum.Client(email="", password="", secret="", code="", token="", proxy_host=None, proxy_port=None, user_agent="random", locale="en-US", log=True)
```

```
# HTTP API
bot.connectionTest()
bot.snowflake_to_unixts(snowflake)
bot.unixts_to_snowflake(unixts)
bot.login(email, password, undelete=False, captcha=None, source=None, gift_code_sku_id=None, secret="", code="")
bot.getXFingerprint()
bot.getBuildNumber()
bot.getSuperProperties(user_agent, buildnum="request")
bot.getGatewayUrl()
bot.getDiscordStatus()
bot.getDetectables()
bot.getOauth2Tokens()
bot.getVersionStableHash(underscore=None)
bot.createDM(recipients)
bot.getMessages(channelID,num=1,beforeDate=None,aroundMessage=None)
bot.getMessage(channelID, messageID)
bot.sendMessage(channelID, message, nonce="calculate", tts=False, embed=None, message_reference=None, allowed_mentions=None, sticker_ids=None)
bot.sendFile(channelID,filelocation,isurl=False,message="", tts=False, message_reference=None, sticker_ids=None)
bot.reply(channelID, messageID, message, nonce="calculate", tts=False, embed=None, allowed_mentions={"parse":["users","roles","everyone"],"replied_user":False}, sticker_ids=None, file=None, isurl=False)
bot.searchMessages(guildID,channelID=None,userID=None,mentionsUserID=None,has=None,beforeDate=None,afterDate=None,textSearch=None,afterNumResults=None)
bot.filterSearchResults(searchResponse)
bot.typingAction(channelID)
bot.deleteMessage(channelID,messageID)
bot.editMessage(channelID,messageID,newMessage)
bot.pinMessage(channelID,messageID)
bot.unPinMessage(channelID,messageID)
bot.getPins(channelID)
bot.addReaction(channelID,messageID,emoji)
bot.removeReaction(channelID,messageID,emoji)
bot.ackMessage(channelID,messageID,ackToken=None)
bot.unAckMessage(channelID,messageID,numMentions=0)
bot.bulkAck(data)
bot.getTrendingGifs(provider="tenor", locale="en-US", media_format="mp4")
bot.getStickers(directoryID="758482250722574376", store_listings=False, locale="en-US")
bot.getStickerFile(stickerID, stickerAsset)
bot.getStickerJson(stickerID, stickerAsset)
bot.getStickerPack(stickerPackID)
bot.requestFriend(user)
bot.acceptFriend(userID)
bot.removeRelationship(userID)
bot.blockUser(userID)
bot.setStatus(status)
bot.setAvatar(imagePath)
bot.setUsername(username)
bot.setEmail(email)
bot.setPassword(new_password)
bot.setDiscriminator(discriminator)
bot.getProfile(userID)
bot.info(with_analytics_token=None)
bot.getUserAffinities()
bot.getGuildAffinities()
bot.getMentions(limit=25, roleMentions=True, everyoneMentions=True)
bot.removeMentionFromInbox(messageID)
bot.setHypesquad(house)
bot.leaveHypesquad()
bot.setLocale(locale)
bot.calculateTOTPcode(secret="default")
bot.getTOTPurl(secret): #use this to store your totp secret/qr pic; btw url format is otpauth://totp/Discord
bot.enable2FA()
bot.disable2FA(code="calculate", clearSecretAfter=False)
bot.getRTCregions()
bot.setAFKtimeout(timeout_seconds)
bot.setTheme(theme)
bot.setMessageDisplay(CozyOrCompact)
bot.enableDevMode(enable)
bot.activateApplicationTestMode(applicationID)
bot.getApplicationData(applicationID, with_guild=False)
bot.getBackupCodes(regenerate=False)
bot.enableInlineMedia(enable)
bot.enableLargeImagePreview(enable)
bot.enableGifAutoPlay(enable)
bot.enableLinkPreview(enable)
bot.enableReactionRendering(enable)
bot.enableAnimatedEmoji(enable)
bot.enableEmoticonConversion(enable)
bot.setStickerAnimation(setting)
bot.enableTTS(enable)
bot.getBillingHistory(limit=20)
bot.getPaymentSources()
bot.getBillingSubscriptions()
bot.getStripeClientSecret()
bot.logout(provider=None, voip_provider=None)
bot.getInfoFromInviteCode(inviteCode)
bot.joinGuild(inviteCode)
bot.leaveGuild(guildID)
bot.createInvite(channelID, max_age_seconds=False, max_uses=False, grantTempMembership=False, checkInvite="", targetType="")
bot.kick(guildID,userID,reason="")
bot.ban(guildID,userID,deleteMessagesDays=0,reason="")
bot.revokeBan(guildID, userID)
bot.getGuildMember(guildID,userID)
bot.getMemberVerificationData(guildID, with_guild=False, invite_code=None)
bot.agreeGuildRules(guildID, form_fields, version="2021-01-31T02:41:24.540000+00:00")
bot.science(events)
bot.calculateClientUUID(eventNum="default", userID="default", increment=True)
bot.refreshClientUUID(resetEventNum=True)
bot.parseClientUUID(client_uuid)
```

```
# Gateway API
bot.gateway.command()
bot.gateway.removeCommand(function, exactMatch=True, allMatches=False)
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
bot.gateway.fetchMembers(guild_id, channel_id, method="overlap", keep=[], considerUpdates=True, startIndex=0, stopIndex=1000000000, reset=True, wait=None, priority=0)
bot.gateway.getMemberFetchingParams(targetRangeStarts)
bot.gateway.finishedMemberFetching(guild_id)
bot.gateway.request.lazyGuild(guild_id, channel_ranges, typing=None, threads=None, activities=None, members=None)
bot.gateway.request.searchGuildMembers(guild_ids, query, limit=10, presences=True)
resp.parsed.guild_member_list_update()
resp.parsed.message_create()
bot.gateway.request.DMchannel(channel_id)
bot.gateway.request.call(channelID, guildID=None, mute=False, deaf=False, video=False)
bot.gateway.request.endCall()
```

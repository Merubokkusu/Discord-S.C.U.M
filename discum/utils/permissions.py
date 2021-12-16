class PERMS:
	'''
	https://discord.com/developers/docs/topics/permissions#permissions-bitwise-permission-flags
	'''
	# Name                      Value           Description
	CREATE_INSTANT_INVITE       = 1 << 0 #      Allows creation of instant invites
	KICK_MEMBERS                = 1 << 1 #      Allows kicking members
	BAN_MEMBERS                 = 1 << 2 #      Allows banning members
	ADMINISTRATOR               = 1 << 3 #      Allows all permissions and bypasses channel permission overwrites
	MANAGE_CHANNELS             = 1 << 4 #      Allows management and editing of channels
	MANAGE_GUILD                = 1 << 5 #      Allows management and editing of the guild
	ADD_REACTIONS               = 1 << 6 #      Allows for the addition of reactions to messages
	VIEW_AUDIT_LOG              = 1 << 7 #      Allows for viewing of audit logs
	PRIORITY_SPEAKER            = 1 << 8 #      Allows for using priority speaker in a voice channel
	STREAM                      = 1 << 9 #      Allows the user to go live
	VIEW_CHANNEL                = 1 << 10 #     Allows guild members to view a channel, which includes reading messages in text channels
	SEND_MESSAGES               = 1 << 11 #     Allows for sending messages in a channel (does not allow sending messages in threads)
	SEND_TTS_MESSAGES           = 1 << 12 #     Allows for sending of /tts messages
	MANAGE_MESSAGES             = 1 << 13 #     Allows for deletion of other users messages
	EMBED_LINKS                 = 1 << 14 #     Links sent by users with this permission will be auto-embedded
	ATTACH_FILES                = 1 << 15 #     Allows for uploading images and files
	READ_MESSAGE_HISTORY        = 1 << 16 #     Allows for reading of message history
	MENTION_EVERYONE            = 1 << 17 #     Allows for using the @everyone tag to notify all users in a channel, and the @here tag to notify all online users in a channel
	USE_EXTERNAL_EMOJIS         = 1 << 18 #     Allows the usage of custom emojis from other servers
	VIEW_GUILD_INSIGHTS         = 1 << 19 #     Allows for viewing guild insights
	CONNECT                     = 1 << 20 #     Allows for joining of a voice channel
	SPEAK                       = 1 << 21 #     Allows for speaking in a voice channel
	MUTE_MEMBERS                = 1 << 22 #     Allows for muting members in a voice channel
	DEAFEN_MEMBERS              = 1 << 23 #     Allows for deafening of members in a voice channel
	MOVE_MEMBERS                = 1 << 24 #     Allows for moving of members between voice channels
	USE_VAD                     = 1 << 25 #     Allows for using voice-activity-detection in a voice channel
	CHANGE_NICKNAME             = 1 << 26 #     Allows for modification of own nickname
	MANAGE_NICKNAMES            = 1 << 27 #     Allows for modification of other users nicknames
	MANAGE_ROLES                = 1 << 28 #     Allows management and editing of roles
	MANAGE_WEBHOOKS             = 1 << 29 #     Allows management and editing of webhooks
	MANAGE_EMOJIS_AND_STICKERS  = 1 << 30 #     Allows management and editing of emojis and stickers
	USE_APPLICATION_COMMANDS    = 1 << 31 #     Allows members to use application commands, including slash commands and context menu commands
	REQUEST_TO_SPEAK            = 1 << 32 #     Allows for requesting to speak in stage channels
	MANAGE_EVENTS               = 1 << 33 #     Allows for creating, editing, and deleting scheduled events
	MANAGE_THREADS              = 1 << 34 #     Allows for deleting and archiving threads, and viewing all private threads
	CREATE_PUBLIC_THREADS       = 1 << 35 #     Allows for creating threads
	CREATE_PRIVATE_THREADS      = 1 << 36 #     Allows for creating private threads
	USE_EXTERNAL_STICKERS       = 1 << 37 #     Allows the usage of custom stickers from other servers
	SEND_MESSAGES_IN_THREADS    = 1 << 38 #     Allows for sending messages in threads
	START_EMBEDDED_ACTIVITIES   = 1 << 39 #     Allows for launching activities (applications with the EMBEDDED flag in a voice channel)
	ALL                         = 1099511627775#All the perms

class Permissions:
	@staticmethod
	def checkPermissions(permissions, check):
		return (permissions & check) == check

	@staticmethod
	def getPermissions(permissions):
		allperms = ['ADD_REACTIONS', 'ADMINISTRATOR', 'ATTACH_FILES', 'BAN_MEMBERS', 'CHANGE_NICKNAME', 'CONNECT', 'CREATE_INSTANT_INVITE', 'CREATE_PRIVATE_THREADS', 'CREATE_PUBLIC_THREADS', 'DEAFEN_MEMBERS', 'EMBED_LINKS', 'KICK_MEMBERS', 'MANAGE_CHANNELS', 'MANAGE_EMOJIS_AND_STICKERS', 'MANAGE_EVENTS', 'MANAGE_GUILD', 'MANAGE_MESSAGES', 'MANAGE_NICKNAMES', 'MANAGE_ROLES', 'MANAGE_THREADS', 'MANAGE_WEBHOOKS', 'MENTION_EVERYONE', 'MOVE_MEMBERS', 'MUTE_MEMBERS', 'PRIORITY_SPEAKER', 'READ_MESSAGE_HISTORY', 'REQUEST_TO_SPEAK', 'SEND_MESSAGES', 'SEND_MESSAGES_IN_THREADS', 'SEND_TTS_MESSAGES', 'SPEAK', 'START_EMBEDDED_ACTIVITIES', 'STREAM', 'USE_APPLICATION_COMMANDS', 'USE_EXTERNAL_EMOJIS', 'USE_EXTERNAL_STICKERS', 'USE_VAD', 'VIEW_AUDIT_LOG', 'VIEW_CHANNEL', 'VIEW_GUILD_INSIGHTS']
		perms = []
		for p in allperms:
			if Permissions.checkPermissions(permissions, getattr(PERMS, p)):
				perms.append(p)
		return perms

	#copied the code from https://discord.com/developers/docs/topics/permissions#permission-overwrites and played around with it
	@staticmethod
	def calculateBasePerms(memberID, guildID, guildOwnerID, guildRoles, memberRoles):
		if memberID == guildOwnerID:
			return PERMS.ALL

		permissions = int(guildRoles[guildID]["permissions"])

		for memberRoleID in memberRoles:
			permissions |= int(guildRoles[memberRoleID]["permissions"])

		if permissions & PERMS.ADMINISTRATOR == PERMS.ADMINISTRATOR:
			return PERMS.ALL

		return permissions

	@staticmethod
	def calculateOverwrites(memberID, guildID, basePermissions, channelOverwrites, memberRoles):
		# ADMINISTRATOR overrides any potential permission overwrites, so there is nothing to do here.
		if basePermissions & PERMS.ADMINISTRATOR == PERMS.ADMINISTRATOR:
			return PERMS.ALL

		permissions = basePermissions
		channelEveryoneOverwrites = next((i for i in channelOverwrites if i["id"]==guildID), False) #https://stackoverflow.com/a/8653568/14776493
		if channelEveryoneOverwrites:
			permissions &= ~int(channelEveryoneOverwrites["deny"])
			permissions |= int(channelEveryoneOverwrites["allow"])

		# Apply role specific overwrites.
		allow = 0
		deny = 0
		for memberRoleID in memberRoles: #for the pertinent roles
			overwriteRole = next((i for i in channelOverwrites if i["id"]==memberRoleID), False) #get the corresponding channel overrides
			if overwriteRole:
				allow |= int(overwriteRole["allow"])
				deny |= int(overwriteRole["deny"])

		permissions &= ~deny
		permissions |= allow

		# Apply member specific overwrite if it exist.
		overwriteMember = next((i for i in channelOverwrites if i["id"]==memberID), False)
		if overwriteMember:
			permissions &= ~int(overwriteMember["deny"])
			permissions |= int(overwriteMember["allow"])

		return permissions

	@staticmethod
	def calculatePermissions(memberID, guildID, guildOwnerID, guildRoles, memberRoles, channelOverwrites): #guildRoles (dictionary), memberRoles(list of strings), channelOverwrites (list of dictionaries)
		basePermissions = Permissions.calculateBasePerms(memberID, guildID, guildOwnerID, guildRoles, memberRoles)
		return Permissions.calculateOverwrites(memberID, guildID, basePermissions, channelOverwrites, memberRoles)

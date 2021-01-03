#points to commands that help request info/actions using the gateway

class GuildRequest(object):
	def __init__(self, gatewayobject):
		self.gatewayobject = gatewayobject

	def lazyGuild(self, guild_id, channel_ranges, typing=None, threads=None, activities=None, members=None): #https://arandomnewaccount.gitlab.io/discord-unofficial-docs/lazy_guilds.html
		data = {
		    "op": self.gatewayobject.OPCODE.LAZY_REQUEST,
		    "d": {
		        "guild_id": guild_id,
		        "typing": typing,
		        "threads": threads,
		        "activities": activities,
		        "members": members,
		        "channels": channel_ranges,
		    },
		}
		if typing == None:
			data["d"].pop("typing")
		if threads == None:
			data["d"].pop("threads")
		if activities == None:
			data["d"].pop("activities")
		if members == None:
			data["d"].pop("members")
		self.gatewayobject.send(data)

	def searchGuildMembers(self, guild_ids, query, limit=10, presences=True):
		if isinstance(guild_ids, str):
			guild_ids = [guild_ids]
		self.gatewayobject.send({"op":self.gatewayobject.OPCODE.REQUEST_GUILD_MEMBERS,"d":{"guild_id":guildIDs,"query":query,"limit":limit,"presences":presences}})
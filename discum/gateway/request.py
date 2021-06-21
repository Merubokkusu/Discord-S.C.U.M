#points to commands that help request info/actions using the gateway
from .guild.request import GuildRequest
from .dms.request import DmRequest
from .user.request import UserRequest
from .media.request import MediaRequest

class Request(object):
	def __init__(self, gatewayobject):
		self.gatewayobject = gatewayobject #remember that the requests session obj is also passed in here

	def setStatus(self, status, activities=[], afk=False, since=0):
		UserRequest(self.gatewayobject).setStatus(status, activities, afk, since)

	def lazyGuild(self, guild_id, channel_ranges=None, typing=None, threads=None, activities=None, members=None, thread_member_lists=None):
		GuildRequest(self.gatewayobject).lazyGuild(guild_id, channel_ranges, typing, threads, activities, members, thread_member_lists)

	def searchGuildMembers(self, guild_ids, query="", limit=10, presences=True, user_ids=None):
		GuildRequest(self.gatewayobject).searchGuildMembers(guild_ids, query, limit, presences, user_ids)

	def DMchannel(self, channel_id):
		DmRequest(self.gatewayobject).DMchannel(channel_id)

	def call(self, channelID, guildID=None, mute=False, deaf=False, video=False):
		MediaRequest(self.gatewayobject).call(channelID, guildID, mute, deaf, video)

	def endCall(self):
		MediaRequest(self.gatewayobject).endCall()
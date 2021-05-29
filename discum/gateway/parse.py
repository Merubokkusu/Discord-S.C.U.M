#parses response from gateway
from .start.parse import StartParse
from .guild.parse import GuildParse
from .user.parse import UserParse
from .messages.parse import MessageParse
from .channels.parse import ChannelParse

import copy

#function names are just lowercase types, so for type GUILD_MEMBER_LIST_UPDATE, the function is guild_member_list_update
class Parse(object):
	def __init__(self, response):
		self.response = copy.deepcopy(response)

	def auto(self): #auto parse, does not allow for custom inputs
		if hasattr(self, str(self.response['t']).lower()):
			return getattr(self, str(self.response['t']).lower())()
		return self.response['d'] #just return the value of d if there's no parse function for it yet

	def ready(self):
		return StartParse.ready(self.response)

	def ready_supplemental(self):
		return StartParse.ready_supplemental(self.response)

	def guild_member_list_update(self):
		return GuildParse.guild_member_list_update(self.response)

	def guild_create(self, my_user_id="0"): #personal user id needed to update personal roles for that guild
		return GuildParse.guild_create(self.response, my_user_id)

	def guild_members_chunk(self):
		return GuildParse.guild_members_chunk(self.response)

	def message_create(self):
		return MessageParse.message_create(self.response)

	def sessions_replace(self, session_id="0"):
		return UserParse.sessions_replace(self.response, session_id)

	def channel_create(self):
		return ChannelParse.channel_create(self.response)

	def channel_delete(self):
		return ChannelParse.channel_delete(self.response)

#parses response from gateway
from .guild.parse import GuildParse
from .messages.parse import MessageParse

#function names are just lowercase types, so for type GUILD_MEMBER_LIST_UPDATE, the function is guild_member_list_update
class Parse(object):
	def __init__(self, response):
		self.response = response

	def auto(self): #auto parse, does not allow for custom inputs
		if hasattr(self, self.response['t'].lower()):
			return getattr(self, self.response['t'].lower())()
		return self.response['d'] #just return the value of d if there's no parse function for it yet

	def guild_member_list_update(self):
		return GuildParse.guild_member_list_update(self.response)

	def message_create(self):
		return MessageParse.message_create(self.response)

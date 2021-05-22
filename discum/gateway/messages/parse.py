from ..types import Types

#parse
class MessageParse(object):
	@staticmethod
	def message_create(response):
		message = dict(response["d"])
		message["type"] = Types.msgTypes[response["d"]["type"]] #number to str
		return message
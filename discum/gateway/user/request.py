#request

class UserRequest(object):
	def __init__(self, gatewayobject):
		self.gatewayobject = gatewayobject

	def setStatus(self, status, activities, afk, since): #note, custom status goes in activities
		data = {
		    "op": self.gatewayobject.OPCODE.PRESENCE_UPDATE,
		    "d": {
		        "status": status,
		        "since": since,
		        "activities": activities,
		        "afk": afk
		    }
		}
		self.gatewayobject.send(data)
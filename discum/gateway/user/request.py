#request

class UserRequest(object):
	__slots__ = ['gatewayobj']
	def __init__(self, gatewayobj):
		self.gatewayobj = gatewayobj

	def setStatus(self, status, activities, afk, since): #note, custom status goes in activities
		data = {
		    "op": self.gatewayobj.OPCODE.PRESENCE_UPDATE,
		    "d": {
		        "status": status,
		        "since": since,
		        "activities": activities,
		        "afk": afk
		    }
		}
		self.gatewayobj.send(data)
#request

class DmRequest(object):
	__slots__ = ['gatewayobj']
	def __init__(self, gatewayobj):
		self.gatewayobj = gatewayobj

	def DMchannel(self, channel_id):
		self.gatewayobj.send({"op":self.gatewayobj.OPCODE.DM_UPDATE,"d":{"channel_id":channel_id}})
#request

class DmRequest(object):
	def __init__(self, gatewayobject):
		self.gatewayobject = gatewayobject

	def DMchannel(self, channel_id):
		self.gatewayobject.send({"op":self.gatewayobject.OPCODE.DM_UPDATE,"d":{"channel_id":channel_id}})
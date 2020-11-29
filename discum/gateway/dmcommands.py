#just a bunch of wrappers

class dmcommands:
	def __init__(self, gatewayobject):
		self.gateway = gatewayobject

	#send
	def listen(self, channelID): #I think you only need to send 1 of these per session, but I could be wrong...
		self.gateway.send({"op":13,"d":{"channel_id":channelID}})


	#event (receive)

	#combos
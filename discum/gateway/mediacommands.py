#just a bunch of wrappers
class mediacommands:
	def __init__(self, gatewayobject):
		self.gateway = gatewayobject

	#send
	def call(self, channelID, guildID=None, mute=False, deaf=False, video=False):
		self.gateway.send({"op":4,"d":{"guild_id":guildID,"channel_id":channelID,"self_mute":mute,"self_deaf":deaf,"self_video":video}})

	def endCalls(self): #ends all calls. you can't be in more than 1 call at the same time
		self.gateway.send({"op":4,"d":{"guild_id":None,"channel_id":None,"self_mute":False,"self_deaf":False,"self_video":False}})


	#event (receive)

	#combos
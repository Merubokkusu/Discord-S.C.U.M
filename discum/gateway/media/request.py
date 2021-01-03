#request

class MediaRequest(object):
	def __init__(self, gatewayobject):
		self.gatewayobject = gatewayobject

	def call(self, channelID, guildID=None, mute=False, deaf=False, video=False):
		self.gatewayobject.send(
		    {
		        "op": self.gatewayobject.OPCODE.VOICE_STATE_UPDATE,
		        "d": {
		            "guild_id": guildID,
		            "channel_id": channelID,
		            "self_mute": mute,
		            "self_deaf": deaf,
		            "self_video": video,
		        },
		    }
		)

	def endCall(self):
		self.gatewayobject.send(
		    {
		        "op": self.gatewayobject.OPCODE.VOICE_STATE_UPDATE,
		        "d": {
		            "guild_id": None,
		            "channel_id": None,
		            "self_mute": False,
		            "self_deaf": False,
		            "self_video": False,
		        },
		    }
		)


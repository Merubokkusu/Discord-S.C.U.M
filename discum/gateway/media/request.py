#request

class MediaRequest(object):
	__slots__ = ['gatewayobj']
	def __init__(self, gatewayobj):
		self.gatewayobj = gatewayobj

	def call(self, channelID, guildID=None, mute=False, deaf=False, video=False):
		self.gatewayobj.send(
		    {
		        "op": self.gatewayobj.OPCODE.VOICE_STATE_UPDATE,
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
		self.gatewayobj.send(
		    {
		        "op": self.gatewayobj.OPCODE.VOICE_STATE_UPDATE,
		        "d": {
		            "guild_id": None,
		            "channel_id": None,
		            "self_mute": False,
		            "self_deaf": False,
		            "self_video": False,
		        },
		    }
		)


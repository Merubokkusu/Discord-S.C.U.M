from ..RESTapiwrap import Wrapper

class Buttons(object):
	__slots__ = ['discord', 's', 'log']
	def __init__(self, discord, s, log):
		self.discord = discord
		self.s = s
		self.log = log

	#click on a button or select menu option(s)
	def click(self, applicationID, channelID, messageID, messageFlags, guildID, nonce, data):
		url = self.discord+"interactions"
		if nonce == "calculate":
			from ..utils.nonce import calculateNonce
			nonce = calculateNonce()
		else:
			nonce = str(nonce)
		body = {
			"type": 3,
			"nonce": nonce,
			"guild_id": guildID,
			"channel_id": channelID,
			"message_flags": messageFlags,
			"message_id": messageID,
			"application_id": applicationID,
			"data": data,
		}
		if guildID == None:
			body.pop("guild_id")
		return Wrapper.sendRequest(self.s, 'post', url, body, log=self.log)
from ..RESTapiwrap import Wrapper

class SlashCommands(object):
	__slots__ = ['discord', 's', 'log']
	def __init__(self, discord, s, log):
		self.discord = discord
		self.s = s
		self.log = log

	def getSlashCommands(self, applicationID):
		url = self.discord+"applications/"+applicationID+"/commands"
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	def triggerSlashCommand(self, applicationID, channelID, guildID, data, nonce):
		url = self.discord+"interactions"
		if nonce == "calculate":
			from ..utils.nonce import calculateNonce
			nonce = calculateNonce()
		else:
			nonce = str(nonce)
		body = {
			"type": 2,
			"application_id": applicationID,
			"guild_id": guildID,
			"channel_id": channelID,
			"data": data,
			"nonce": nonce,
		}
		if guildID == None:
			body.pop("guild_id")
		return Wrapper.sendRequest(self.s, 'post', url, body, log=self.log)
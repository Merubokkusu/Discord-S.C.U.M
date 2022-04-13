import random, string
from requests_toolbelt import MultipartEncoder
import json

from ..utils.nonce import calculateNonce
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

	def triggerSlashCommand(self, applicationID, channelID, guildID, data, nonce, sessionID):
		url = self.discord+"interactions"
		#nonce
		if nonce == "calculate":
			nonce = calculateNonce("now")
		else:
			nonce = str(nonce)
		#session id
		if sessionID == "random":
			sessionID = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
		#body
		payload = {
			"type": 2,
			"application_id": applicationID,
			"guild_id": guildID,
			"channel_id": channelID,
			"data": data,
			"nonce": nonce,
			"session_id": sessionID
		}
		if guildID == None:
			payload.pop("guild_id")
		fields = {"payload_json":(None, json.dumps(payload))}
		randomstr = ''.join(random.sample(string.ascii_letters+string.digits,16))
		body = MultipartEncoder(fields=fields, boundary='----WebKitFormBoundary'+randomstr)
		headerMods = {"update": {"Content-Type": body.content_type}}

		return Wrapper.sendRequest(self.s, 'post', url, body, headerModifications=headerMods, log=self.log)



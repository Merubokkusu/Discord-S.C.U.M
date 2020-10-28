import requests
import json
from ..Logger import *
import urllib

class Guild(object):
	def __init__(self, discord, s): #s is the requests session object
		self.discord = discord
		self.s = s

	'''
	invite codes / server info
	'''
	#get guild info from invite code
	def getInfoFromInviteCode(self,inviteCode):
		url = self.discord+f"invites/{inviteCode}?with_counts=true"
		Logger.LogMessage('Get -> {}'.format(url))
		response = self.s.get(url)
		Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
		return response

	#join guild with invite code
	def joinGuild(self,inviteCode):
		url = self.discord+"invites/"+inviteCode
		Logger.LogMessage('Post -> {}'.format(url))
		response = self.s.get(url)
		Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
		return response

	'''
	server moderation
	'''
	#kick a user
	def kickUser(self,guildID,userID,reason):
		url = self.discord+f"guilds/{guildID}/members/{userID}?reason={urllib.parse.quote(reason)}"
		Logger.LogMessage('Delete -> {}'.format(url))
		response = self.s.delete(url)
		Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
		return response

	#ban a user
	def banUser(self,guildID,userID,deleteMessagesDays,reason):
		url = self.discord+f"guilds/{guildID}/bans/{userID}"
		body = {"delete_message_days": str(deleteMessagesDays), "reason": reason}
		Logger.LogMessage('Put -> {}'.format(url))
		Logger.LogMessage('{}'.format(str(body)))
		response = self.s.put(url, data=json.dumps(body))
		Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
		return response
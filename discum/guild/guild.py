import requests
import json
from ..Logger import *
import urllib

class Guild(object):
	def __init__(self, discord, s, log): #s is the requests session object
		self.discord = discord
		self.s = s
		self.log = log

	'''
	invite codes / server info
	'''
	#get guild info from invite code
	def getInfoFromInviteCode(self,inviteCode):
		url = self.discord+f"invites/{inviteCode}?with_counts=true"
		if self.log: Logger.LogMessage('Get -> {}'.format(url))
		response = self.s.get(url)
		if self.log: Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
		return response

	#join guild with invite code
	def joinGuild(self,inviteCode):
		url = self.discord+"invites/"+inviteCode
		if self.log: Logger.LogMessage('Post -> {}'.format(url))
		response = self.s.get(url)
		if self.log: Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
		return response

	'''
	server moderation
	'''
	#kick a user
	def kick(self,guildID,userID,reason):
		url = self.discord+f"guilds/{guildID}/members/{userID}?reason={urllib.parse.quote(reason)}"
		if self.log: Logger.LogMessage('Delete -> {}'.format(url))
		response = self.s.delete(url)
		if self.log: Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
		return response

	#ban a user
	def ban(self,guildID,userID,deleteMessagesDays,reason):
		url = self.discord+f"guilds/{guildID}/bans/{userID}"
		body = {"delete_message_days": str(deleteMessagesDays), "reason": reason}
		if self.log: Logger.LogMessage('Put -> {}'.format(url))
		if self.log: Logger.LogMessage('{}'.format(str(body)))
		response = self.s.put(url, data=json.dumps(body))
		if self.log: Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
		return response

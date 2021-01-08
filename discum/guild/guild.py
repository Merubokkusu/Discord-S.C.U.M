from ..RESTapiwrap import *

if __import__('sys').version.split(' ')[0] < '3.0.0':
    from urllib import quote
else:
    from urllib.parse import quote

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
		url = self.discord+"invites/"+inviteCode+"?with_counts=true"
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	#join guild with invite code
	def joinGuild(self,inviteCode):
		url = self.discord+"invites/"+inviteCode
		return Wrapper.sendRequest(self.s, 'post', url, log=self.log)

	'''
	server moderation
	'''
	#kick a user
	def kick(self,guildID,userID,reason):
		url = self.discord+"guilds/%s/members/%s?reason=%s" % (guildID, userID, quote(reason))
		return Wrapper.sendRequest(self.s, 'delete', url, log=self.log)

	#ban a user
	def ban(self,guildID,userID,deleteMessagesDays,reason):
		url = self.discord+"guilds/%s/bans/%s" % (guildID, userID)
		body = {"delete_message_days": str(deleteMessagesDays), "reason": reason}
		return Wrapper.sendRequest(self.s, 'put', url, body, log=self.log)

	#lookup a user in a guild. thx Echocage for finding this api endpoint
	'''Note, user clients do not run this api request, however it currently works without a problem. 
	Once discum's gatewayserver is improved, we'll add the actual api to discum (to best mimic the web client)
	'''
	def getGuildMember(self, guildID, userID):
		url = self.discord+"/guilds/%s/members/%s" % (guildID, userID)
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

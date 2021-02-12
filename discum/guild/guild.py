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

	def leaveGuild(self, guildID):
		url = self.discord+"users/@me/guilds/"+guildID
		return Wrapper.sendRequest(self.s, 'delete', url, log=self.log)

	def createInvite(self, channelID, max_age_seconds, max_uses, grantTempMembership, checkInvite, targetType): #has to be a channel thats in a guild. also checkInvite and targetType are basically useless.
		url = self.discord+"channels/"+channelID+"/invites"
		if max_age_seconds == False:
			max_age_seconds = 0
		if max_uses == False:
			max_uses = 0
		body = {"max_age": max_age_seconds, "max_uses": max_uses, "temporary": grantTempMembership}
		if checkInvite != "":
			body["validate"] = checkInvite
		if targetType != "":
			body["target_type"] = targetType
		return Wrapper.sendRequest(self.s, 'post', url, body, log=self.log)

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

	def revokeBan(self, guildID, userID):
		url = self.discord+"guilds/"+guildID+"/bans/"+userID
		return Wrapper.sendRequest(self.s, 'delete', url, log=self.log)



	#lookup a user in a guild. thx Echocage for finding this api endpoint
	'''Note, user clients do not run this api request, however it currently works without a problem. 
	Once the equivalent gateway command/request is added, the getGuildMember function will be removed from here.
	'''
	def getGuildMember(self, guildID, userID):
		url = self.discord+"/guilds/%s/members/%s" % (guildID, userID)
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	#get member verification data
	def getMemberVerificationData(self, guildID, with_guild=False, invite_code=None):
		url = "https://discord.com/api/v8/guilds/"+guildID+"/member-verification?with_guild="+str(with_guild).lower()
		if invite_code != None:
			url += "&invite_code="+invite_code
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	def agreeGuildRules(self, guildID, form_fields, version):
		url = "https://discord.com/api/v8/guilds/"+guildID+"/requests/@me"
		form_fields[0]['response'] = True
		body = {"version":version, "form_fields":json.dumps(form_fields)}
		return Wrapper.sendRequest(self.s, 'put', url, body, log=self.log)

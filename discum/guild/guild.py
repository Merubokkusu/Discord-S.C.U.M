from ..RESTapiwrap import *
from ..utils.permissions import PERMS, Permissions
from ..utils.contextproperties import ContextProperties

import time

try:
	from urllib.parse import quote
except ImportError:
	from urllib import quote

class Guild(object):
	def __init__(self, discord, s, log): #s is the requests session object
		self.discord = discord
		self.s = s
		self.log = log

	'''
	invite codes / server info
	'''
	#get guild info from invite code
	def getInfoFromInviteCode(self, inviteCode, with_counts, with_expiration, fromJoinGuildNav):
		url = self.discord+"invites/"+inviteCode
		if (with_counts!=None or with_expiration!=None or fromJoinGuildNav):
			url += "?"
			data = {}
			if fromJoinGuildNav:
				data["inputValue"] = inviteCode
			if with_counts != None:
				data["with_counts"] = with_counts
			if with_expiration != None:
				data["with_expiration"] = with_expiration
			url += "&".join( "%s=%s" % (k, quote(repr(data[k]).lower())) for k in data)
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	#just the join guild endpoint, default location mimics joining a guild from the ([+]Add a Server) button
	def joinGuildRaw(self, inviteCode, guild_id, channel_id, channel_type, location="join guild"):
		url = self.discord+"invites/"+inviteCode
		return Wrapper.sendRequest(self.s, 'post', url, headerModifications={"update":{"X-Context-Properties":ContextProperties.get(location, guild_id=guild_id, channel_id=channel_id, channel_type=channel_type)}}, log=self.log)

	def joinGuild(self, inviteCode, location, wait):
		guildData = self.getInfoFromInviteCode(inviteCode, with_counts=True, with_expiration=True, fromJoinGuildNav=(location.lower()=="join guild")).json()
		if wait: time.sleep(wait)
		return self.joinGuildRaw(inviteCode, guildData["guild"]["id"], guildData["channel"]["id"], guildData["channel"]["type"], location)

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
		return Wrapper.sendRequest(self.s, 'post', url, body, headerModifications={"update":{"X-Context-Properties":ContextProperties.get("guild header")}}, log=self.log)

	def getGuilds(self, with_counts):
		url = self.discord+"users/@me/guilds"
		if with_counts != None:
			url += "?with_counts="+repr(with_counts).lower()
		return Wrapper.sendRequest(self.s, 'get', url, headerModifications={"update":{"X-Track":self.s.headers.get("X-Super-Properties")}, "remove":"X-Super-Properties"}, log=self.log)

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
		url = self.discord+"guilds/%s/members/%s" % (guildID, userID)
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	#get member verification data
	def getMemberVerificationData(self, guildID, with_guild, invite_code):
		url = self.discord+"guilds/"+guildID+"/member-verification?with_guild="+str(with_guild).lower()
		if invite_code != None:
			url += "&invite_code="+invite_code
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	def agreeGuildRules(self, guildID, form_fields, version):
		url = self.discord+"guilds/"+guildID+"/requests/@me"
		form_fields[0]['response'] = True
		body = {"version":version, "form_fields":form_fields}
		return Wrapper.sendRequest(self.s, 'put', url, body, log=self.log)

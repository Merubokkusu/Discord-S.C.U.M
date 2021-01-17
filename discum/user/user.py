import base64
from ..RESTapiwrap import *

class User(object):
	def __init__(self, discord, s, log): #s is the requests session object
		self.discord = discord
		self.s = s
		self.log = log
		
	#def getDMs(self): #websockets does this now
	#	url = self.discord+"users/@me/channels"
	#	return self.s.get(url)

	#def getGuilds(self): #websockets does this now
	#	url = self.discord+"users/@me/guilds"
	#	return self.s.get(url)

	#def getRelationships(self): #websockets does this now
	#	url = self.discord+"users/@me/relationships"
	#	return self.s.get(url)

	def requestFriend(self,user):
		if "#" in user:
			url = self.discord+"users/@me/relationships"
			body = {"username": user.split("#")[0], "discriminator": int(user.split("#")[1])}
			return Wrapper.sendRequest(self.s, 'post', url, body, log=self.log)
		else:
			url = self.discord+"users/@me/relationships/"+user
			body = {}
			return Wrapper.sendRequest(self.s, 'put', url, body, log=self.log)

	def acceptFriend(self,userID):
		url = self.discord+"users/@me/relationships/"+userID
		body = {}
		return Wrapper.sendRequest(self.s, 'put', url, body, log=self.log)

	def removeRelationship(self,userID): #for removing friends, unblocking people
		url = self.discord+"users/@me/relationships/"+userID
		return Wrapper.sendRequest(self.s, 'delete', url, log=self.log)

	def blockUser(self,userID):
		url = self.discord+"users/@me/relationships/"+userID
		body = {"type": 2}
		return Wrapper.sendRequest(self.s, 'put', url, body, log=self.log)

	def getProfile(self,userID):
		url = self.discord+"users/"+userID+"/profile"
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	def me(self, with_analytics_token=None): #simple. bot.me() for own user data
		url = self.discord+"users/@me"
		if with_analytics_token!=None:
			with_analytics_token = str(with_analytics_token).lower()
			url += "?with_analytics_token="+with_analytics_token
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	def getUserAffinities(self):
		url = self.discord+"users/@me/affinities/users"
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	#guild affinities with respect to current user, decided to organize this wrap in here b/c that's how the api is organized
	def getGuildAffinities(self):
		url = self.discord+"users/@me/affinities/guilds"
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	def getMentions(self, limit=25, roleMentions=True, everyoneMentions=True):
		roleMentions = str(roleMentions).lower()
		everyoneMentions = str(everyoneMentions).lower()
		url = self.discord+"users/@me/mentions?limit="+str(limit)+"&roles="+roleMentions+"&everyone="+everyoneMentions
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	def removeMentionFromInbox(self, messageID):
		url = self.discord+"users/@me/mentions/"+messageID
		return Wrapper.sendRequest(self.s, 'delete', url, log=self.log)

	def getMyStickers(self):
		url = self.discord+"users/@me/sticker-packs"
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	'''
	Profile Edits
	'''	
	def setStatus(self,status): #status options are: online, idle, dnd, invisible
		url = self.discord+"users/@me/settings"
		if status in ("online", "idle", "dnd", "invisible"):
			body = {"status": status}
		elif status in ('', None):
			body = {"custom_status": None}
		else:
			body = {"custom_status":{"text": str(status)}}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def setAvatar(self, imagePath): #local image
		url = self.discord+"users/@me"
		with open(imagePath, "rb") as image:
			encodedImage = base64.b64encode(image.read()).decode('utf-8')
		body = {"avatar":"data:image/png;base64,"+encodedImage}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def setUsername(self, username, password):
		url = self.discord+"users/@me"
		body = {"username": username, "password": password}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def setEmail(self, email, password):
		url = self.discord+"users/@me"
		body = {"email": email, "password": password}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def setPassword(self, new_password, password):
		url = self.discord+"users/@me"
		body = {"password": password, "new_password": new_password}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def setDiscriminator(self, discriminator, password):
		url = self.discord+"users/@me"
		body = {"password":password, "discriminator":discriminator}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)


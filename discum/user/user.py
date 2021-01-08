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

	'''
	Profile Edits
	'''
	def changeName(self,email,password,name):
		url = self.discord+"users/@me"
		body = {"username":name,"email":email,"password":password}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)
	
	def setStatus(self,status):
		url = self.discord+"users/@me/settings"
		if(status == 0): # Online
			body = {"status":"online"}
		elif(status == 1): # Idle
			body = {"status":"idle"}
		elif(status == 2): #Do Not Disturb
			body = {"status":"dnd"}
		elif (status == 3): #Invisible
			body = {"status":"invisible"}
		elif (status == ''):
			body = {"custom_status":None}
		else:
			body = {"custom_status":{"text":status}}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def setAvatar(self,email,password,imagePath): #local image path
		url = self.discord+"users/@me"
		with open(imagePath, "rb") as image:
			encodedImage = base64.b64encode(image.read()).decode('utf-8')
		body = {"email":email,"password":password,"avatar":"data:image/png;base64,"+encodedImage,"discriminator":None,"new_password":None}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)
		

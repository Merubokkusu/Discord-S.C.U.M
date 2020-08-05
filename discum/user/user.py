import requests
import json
import base64

class User(object):
	def __init__(self, discord, s): #s is the requests session object
		self.discord = discord
		self.s = s
		
	def getDMs(self):
		url = self.discord+"users/@me/channels"
		return self.s.get(url)

	def getGuilds(self):
		url = self.discord+"users/@me/guilds"
		return self.s.get(url)

	def getRelationships(self):
		url = self.discord+"users/@me/relationships"
		return self.s.get(url)

	def requestFriend(self,userID):
		url = self.discord+"users/@me/relationships/"+userID
		return self.s.put(url, data=json.dumps({}))

	def acceptFriend(self,userID):
		url = self.discord+"users/@me/relationships/"+userID
		return self.s.put(url, data=json.dumps({}))

	def removeRelationship(self,userID): #for removing friends, unblocking people
		url = self.discord+"users/@me/relationships/"+userID
		return self.s.delete(url)

	def blockUser(self,userID):
		url = self.discord+"users/@me/relationships/"+userID
		return self.s.put(url, data=json.dumps({"type":2}))

	'''
	Profile Edits
	'''
	def changeName(self,email,password,name):
		url = self.discord+"users/@me"
		return self.s.patch(url, data=json.dumps({"username":name,"email":email,"password":password}))
	
	def setStatus(self,status):
		url = self.discord+"users/@me/settings"
		if(status == 0): # Online
			return self.s.patch(url, data=json.dumps({"status":"online"}))
		elif(status == 1): # Idle
			return self.s.patch(url, data=json.dumps({"status":"idle"}))
		elif(status == 2): #Do Not Disturb
			return self.s.patch(url, data=json.dumps({"status":"dnd"}))
		elif (status == 3): #Invisible
			return self.s.patch(url, data=json.dumps({"status":"invisible"}))
		elif (status == ''):
			return self.s.patch(url, data=json.dumps({"custom_status":null}))
		else:
			return self.s.patch(url, data=json.dumps({"custom_status":{"text":status}}))

	def setAvatar(self,email,password,imagePath):
		url = self.discord+"users/@me"
		with open(imagePath, "rb") as image:
			encodedImage = base64.b64encode(image.read()).decode('utf-8')
		return self.s.patch(url, data=json.dumps({"email":email,"password":password,"avatar":"data:image/png;base64,"+encodedImage,"discriminator":null,"new_password":null}))
		

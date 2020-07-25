import requests
import json
import base64
true=True
false=False
null=None

class User(object):
	def __init__(self, discord, headers):
		self.discord = discord
		self.headers = headers
		
	def getDMs(self):
		url = self.discord+"users/@me/channels"
		return eval(requests.get(url,headers=self.headers).content)

	def getGuilds(self):
		url = self.discord+"users/@me/guilds"
		return eval(requests.get(url,headers=self.headers).content)

	def getRelationships(self):
		url = self.discord+"users/@me/relationships"
		return eval(requests.get(url,headers=self.headers).content)

	def requestFriend(self,ID):
		url = self.discord+"users/@me/relationships/"+ID
		return requests.put(url,headers=self.headers, data=json.dumps({}))

	def acceptFriend(self,ID):
		url = self.discord+"users/@me/relationships/"+ID
		return requests.put(url,headers=self.headers, data=json.dumps({}))

	def removeRelationship(self,ID): #for removing friends, unblocking people
		url = self.discord+"users/@me/relationships/"+ID
		return requests.delete(url,headers=self.headers)

	def blockUser(self,ID):
		url = self.discord+"users/@me/relationships/"+ID
		return requests.put(url,headers=self.headers, data=json.dumps({"type":2}))

	'''
	Profile Edits
	'''
	def changeName(self,email,password,name):
		url = self.discord+"users/@me"
		return requests.patch(url,headers=self.headers,data=json.dumps({"username":name,"email":email,"password":password}))
	
	def setStatus(self,status):
		url = self.discord+"users/@me/settings"
		if(status == 0): # Online
			return requests.patch(url,headers=self.headers,data=json.dumps({"status":"online"}))
		elif(status == 1): # Idle
			return requests.patch(url,headers=self.headers,data=json.dumps({"status":"idle"}))
		elif(status == 2): #Do Not Disturb
			return requests.patch(url,headers=self.headers,data=json.dumps({"status":"dnd"}))
		elif (status == 3): #Invisible
			return requests.patch(url,headers=self.headers,data=json.dumps({"status":"invisible"}))
		elif (status == ''):
			return requests.patch(url,headers=self.headers,data=json.dumps({"custom_status":null}))
		else:
			return requests.patch(url,headers=self.headers,data=json.dumps({"custom_status":{"text":status}}))

	def setAvatar(self,email,password,imagePath):
		url = self.discord+"users/@me"
		with open(imagePath, "rb") as image:
			encodedImage = base64.b64encode(image.read()).decode('utf-8')
		return requests.patch(url,headers=self.headers,data=json.dumps({"email":email,"password":password,"avatar":"data:image/png;base64,"+encodedImage,"discriminator":null,"new_password":null}))
		
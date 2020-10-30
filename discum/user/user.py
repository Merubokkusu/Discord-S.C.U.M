import requests
import json
import base64
from ..Logger import *

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
			if self.log: Logger.LogMessage('Post -> {}'.format(url))
			if self.log: Logger.LogMessage('{}'.format(str(body)))
			response = self.s.post(url, data=json.dumps(body))
			if self.log: Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
			return response
		url = self.discord+"users/@me/relationships/"+user
		if self.log: Logger.LogMessage('Put -> {}'.format(url))
		response = self.s.put(url, data=json.dumps({}))
		if self.log: Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
		return response

	def acceptFriend(self,userID):
		url = self.discord+"users/@me/relationships/"+userID
		if self.log: Logger.LogMessage('Put -> {}'.format(url))
		response = self.s.put(url, data=json.dumps({}))
		if self.log: Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
		return response

	def removeRelationship(self,userID): #for removing friends, unblocking people
		url = self.discord+"users/@me/relationships/"+userID
		if self.log: Logger.LogMessage('Delete -> {}'.format(url))
		response = self.s.delete(url)
		if self.log: Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
		return response

	def blockUser(self,userID):
		url = self.discord+"users/@me/relationships/"+userID
		if self.log: Logger.LogMessage('Put -> {}'.format(url))
		if self.log: Logger.LogMessage('{}'.format(str({"type":2})))
		response = self.s.put(url, data=json.dumps({"type":2}))
		if self.log: Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
		return response

	'''
	Profile Edits
	'''
	def changeName(self,email,password,name):
		url = self.discord+"users/@me"
		if self.log: Logger.LogMessage('Patch -> {}'.format(url))
		if self.log: Logger.LogMessage('{}'.format(str({"username":name,"email":email,"password":password})))
		response = self.s.patch(url, data=json.dumps({"username":name,"email":email,"password":password}))
		if self.log: Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
		return response
	
	def setStatus(self,status):
		url = self.discord+"users/@me/settings"
		if self.log: Logger.LogMessage('Patch -> {}'.format(url))
		if(status == 0): # Online
			if self.log: Logger.LogMessage('{}'.format(str({"status":"online"})))
			response = self.s.patch(url, data=json.dumps({"status":"online"}))
			if self.log: Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
			return response
		elif(status == 1): # Idle
			if self.log: Logger.LogMessage('{}'.format(str({"status":"idle"})))
			response = self.s.patch(url, data=json.dumps({"status":"idle"}))
			if self.log: Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
			return response
		elif(status == 2): #Do Not Disturb
			if self.log: Logger.LogMessage('{}'.format(str({"status":"dnd"})))
			response = self.s.patch(url, data=json.dumps({"status":"dnd"}))
			if self.log: Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
			return response
		elif (status == 3): #Invisible
			if self.log: Logger.LogMessage('{}'.format(str({"status":"invisible"})))
			response = self.s.patch(url, data=json.dumps({"status":"invisible"}))
			if self.log: Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
			return response
		elif (status == ''):
			if self.log: Logger.LogMessage('{}'.format(str({"custom_status":None})))
			response = self.s.patch(url, data=json.dumps({"custom_status":None}))
			if self.log: Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
			return response
		else:
			if self.log: Logger.LogMessage('{}'.format(str({"custom_status":{"text":status}})))
			response = self.s.patch(url, data=json.dumps({"custom_status":{"text":status}}))
			if self.log: Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
			return response

	def setAvatar(self,email,password,imagePath): #local image path
		url = self.discord+"users/@me"
		if self.log: Logger.LogMessage('Patch -> {}'.format(url))
		if self.log: Logger.LogMessage('{}'.format(str({"email":email,"password":password,"avatar":"data:image/png;base64,<encoded image data>","discriminator":None,"new_password":None})))
		with open(imagePath, "rb") as image:
			encodedImage = base64.b64encode(image.read()).decode('utf-8')
		response = self.s.patch(url, data=json.dumps({"email":email,"password":password,"avatar":"data:image/png;base64,"+encodedImage,"discriminator":None,"new_password":None}))
		if self.log: Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
		return response
		

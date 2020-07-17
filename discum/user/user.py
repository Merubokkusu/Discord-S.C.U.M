import requests
import json
true=True
false=False
null=None

class User(object):
	def __init__(self, headers):
		self.headers = headers
		
	def getDMs(self):
		url = "https://discord.com/api/v6/users/@me/channels"
		return eval(requests.get(url,headers=self.headers).content)

	def getGuilds(self):
		url = "https://discord.com/api/v6/users/@me/guilds"
		return eval(requests.get(url,headers=self.headers).content)

	def getRelationships(self):
		url = "https://discord.com/api/v6/users/@me/relationships"
		return eval(requests.get(url,headers=self.headers).content)

	def requestFriend(self,ID):
		url = "https://discord.com/api/v6/users/@me/relationships/"+ID
		return requests.put(url,headers=self.headers, data=json.dumps({}))

	def acceptFriend(self,ID):
		url = "https://discord.com/api/v6/users/@me/relationships/"+ID
		return requests.put(url,headers=self.headers, data=json.dumps({}))

	def removeRelationship(self,ID): #for removing friends, unblocking people
		url = "https://discord.com/api/v6/users/@me/relationships/"+ID
		return requests.delete(url,headers=self.headers)

	def blockUser(self,ID):
		url = "https://discord.com/api/v6/users/@me/relationships/"+ID
		return requests.put(url,headers=self.headers, data=json.dumps({"type":2}))

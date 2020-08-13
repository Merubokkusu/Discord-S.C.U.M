import requests
import json
from ..fileparse.fileparse import Fileparse
from ..Logger import *
from urllib.parse import urlparse,quote_plus
from requests_toolbelt import MultipartEncoder
import random,string
import math
import os
import time

class Messages(object):
	def __init__(self, discord, s): #s is the requests session object
		self.discord = discord
		self.s = s

	#get Message
	def getMessages(self,channelID,num,beforeDate): # 1 ≤ num ≤ 100, beforeDate is a snowflake
		url = self.discord+"channels/"+channelID+"/messages?limit="+str(num)
		if beforeDate != None:
			url += "&before="+str(beforeDate)
		Logger.LogMessage('Get -> {}'.format(url))
		response = self.s.get(url)
		Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
		return response

	#text message
	def sendMessage(self,channelID,message,embed,tts):
		url = self.discord+"channels/"+channelID+"/messages"
		body = {"content": message, "tts": tts,"embed":embed}
		Logger.LogMessage('Post -> {}'.format(url))
		Logger.LogMessage('{}'.format(str(body)))
		response = self.s.post(url, data=json.dumps(body))
		Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
		return response

	#send file
	def sendFile(self,channelID,filelocation,isurl,message):
		mimetype, extensiontype, fd = Fileparse(self.s).parse(filelocation,isurl) #guess extension from file data
		if mimetype == 'invalid': #error out
			print('ERROR: File does not exist.')
			return
		if isurl: #get filename
			a = urlparse(filelocation)
			if len(os.path.basename(a.path))>0: #if everything is normal...
				filename = os.path.basename(a.path)
			else: 
				if mimetype == 'unsupported': #if filetype not detected and extension not given
					filename = 'unknown'
				else: #if filetype detected but extension not given
					filename = 'unknown.'+extensiontype
		else: #local file
			filename = os.path.basename(os.path.normpath(filelocation))
		#now time to post the file
		url = self.discord+'channels/'+channelID+'/messages'
		if isurl:
			fields={"file":(filename,fd,mimetype),"file_id":"0", "content":message}
		else:
			fields={"file":(filename,open(filelocation,'rb').read(),mimetype),"file_id":"0", "content":message}
		m=MultipartEncoder(fields=fields,boundary='----WebKitFormBoundary'+''.join(random.sample(string.ascii_letters+string.digits,16)))
		self.s.headers.update({"Content-Type":m.content_type})
		Logger.LogMessage('Post -> {}'.format(url))
		Logger.LogMessage('{}'.format(str(MultipartEncoder(fields={"file":(filename,"<file data here>",mimetype),"file_id":"0", "content":message},boundary='----WebKitFormBoundary'+''.join(random.sample(string.ascii_letters+string.digits,16))))))
		response = self.s.post(url, data=m)
		Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
		return response

	def searchMessages(self,guildID,channelID,userID,mentionsUserID,has,beforeDate,afterDate,textSearch,afterNumResults): #classic discord search function, results with key "hit" are the results you searched for, afterNumResults (aka offset) is multiples of 25 and indicates after which messages (type int), filterResults defaults to False
		url = self.discord+"guilds/"+guildID+"/messages/search?"
		queryparams = ""
		if not all(v is None for v in [channelID,userID,mentionsUserID,has,beforeDate,afterDate,textSearch,afterNumResults]):
			if channelID != None and isinstance(channelID,list):
				for item in channelID:
					if isinstance(item,int):
						queryparams += "channel_id="+str(item)+"&"
					elif isinstance(item,str) and len(item)>0:
						queryparams += "channel_id="+item+"&"
			if userID != None and isinstance(userID,list):
				for item in userID:
					if isinstance(item,int):
						queryparams += "author_id="+str(item)+"&"
					elif isinstance(item,str) and len(item)>0:
						queryparams += "author_id="+item+"&"
			if mentionsUserID != None and isinstance(mentionsUserID,list):
				for item in mentionsUserID:
					if isinstance(item,int):
						queryparams += "mentions="+str(item)+"&"
					elif isinstance(item,str) and len(item)>0:
						queryparams += "mentions="+item+"&"
			if has != None and isinstance(has,list):
				for item in has:
					if isinstance(item,str) and len(item)>0:
						queryparams += "has="+item+"&"
			if beforeDate != None and isinstance(beforeDate,int):
				queryparams += "min_id="+str(beforeDate)+"&"
			if afterDate != None and isinstance(afterDate,int):
				queryparams += "max_id="+str(afterDate)+"&"
			if textSearch != None and isinstance(textSearch,str): #textSearch can be len 0....ugh
				queryparams += "content="+quote_plus(textSearch)+"&"
			if afterNumResults != None and isinstance(afterNumResults,int):
				queryparams += "offset="+str(afterNumResults)
			url += queryparams
			Logger.LogMessage('Get -> {}'.format(url))
			response = self.s.get(url)
			Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
			return response
		Logger.LogMessage('Get -> {}'.format(url))
		response = self.s.get(url)
		Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
		return response

	def filterSearchResults(self,searchResponse): #only input is the requests response object outputted from searchMessages, returns type list
		jsonresponse = searchResponse.json()['messages']
		filteredMessages = []
		for group in jsonresponse:
			for result in group:
				if 'hit' in result:
					filteredMessages.append(result)
		return filteredMessages

	def typingAction(self,channelID): #sends the typing action for 10 seconds (or until you change the page)
		url = self.discord+"channels/"+channelID+"/typing"
		Logger.LogMessage('Post -> {}'.format(url))
		response = self.s.post(url)
		Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
		return response

	def editMessage(self,channelID,messageID,newMessage):
		url = self.discord+"channels/"+channelID+"/messages/"+messageID
		body = {"content": newMessage}
		Logger.LogMessage('Patch -> {}'.format(url))
		Logger.LogMessage('{}'.format(str(body)))
		response = self.s.patch(url, data=json.dumps(body))
		Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
		return response

	def deleteMessage(self,channelID,messageID):
		url = self.discord+"channels/"+channelID+"/messages/"+messageID
		Logger.LogMessage('Delete -> {}'.format(url))
		response = self.s.delete(url)
		Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
		return response

	def pinMessage(self,channelID,messageID):
		url = self.discord+"channels/"+channelID+"/pins/"+messageID
		Logger.LogMessage('Put -> {}'.format(url))
		response = self.s.put(url)
		Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
		return response

	def unPinMessage(self,channelID,messageID):
		url = self.discord+"channels/"+channelID+"/pins/"+messageID
		Logger.LogMessage('Delete -> {}'.format(url))
		response = self.s.delete(url)
		Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
		return response

	def getPins(self,channelID): #get pinned messages
		url = self.discord+"channels/"+channelID+"/pins"
		Logger.LogMessage('Get -> {}'.format(url))
		response = self.s.get(url)
		Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
		return response

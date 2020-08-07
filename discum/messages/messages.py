import requests
import json
from ..fileparse.fileparse import Fileparse
from ..Logger import *
from urllib.parse import urlparse
from requests_toolbelt import MultipartEncoder
import random,string
import os

class Messages(object):
	def __init__(self, discord, s): #s is the requests session object
		self.discord = discord
		self.s = s

	#get messages
	def getMessage(self,channelID,num): # num <= 100
		url = self.discord+"channels/"+channelID+"/messages?limit="+str(num)
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

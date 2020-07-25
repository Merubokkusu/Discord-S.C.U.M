import requests
import json
from ..fileparse.fileparse import Fileparse
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from requests_toolbelt import MultipartEncoder
import random,string
import os

class Messages(object):
	def __init__(self, discord, headers):
		self.discord = discord
		self.headers = headers

	#get messages
	def getMessage(self,channelID,num):
		true=True
		false=False
		null=None
		url = self.discord+"channels/"+channelID+"/messages?limit="+str(num)
		return eval(requests.get(url, headers=self.headers).content)

	#text message
	def sendMessage(self,channelID,message,embed,tts):
		url = self.discord+"channels/"+channelID+"/messages"
		body = {"content": message, "tts": tts,'embed':embed}
		return requests.post(url, headers=self.headers, data=json.dumps(body)).content

	#send file
	def sendFile(self,channelID,filelocation,isurl,message):
		mimetype, extensiontype = Fileparse().parse(filelocation,isurl) #guess extension from file data
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
			req = Request(filelocation, headers={'User-Agent': 'Mozilla/5.0'})
			fd = urlopen(req).read()
			fields={'file':(filename,fd,mimetype),'file_id':"0", "content":message}
		else:
			fields={'file':(filename,open(filelocation,'rb').read(),mimetype),'file_id':"0", "content":message}
		m=MultipartEncoder(fields=fields,boundary='----WebKitFormBoundary'+''.join(random.sample(string.ascii_letters+string.digits,16)))
		sendfileheaders = self.headers
		sendfileheaders['Content-Type']=m.content_type
		return requests.post(url, headers=sendfileheaders, data=m).content

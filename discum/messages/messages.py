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

	#search messages (can load all messages or search thru them), talk about mining some data lol
	def getMessages(self,guildID,channelID,userID,mentionsUserID,has,beforeDate,afterDate,textSearch,waitTime):
		url = self.discord+"guilds/"+guildID+"/messages/search?"
		queryparams = ""
		if not all(v is None for v in [channelID,userID,mentionsUserID,has,beforeDate,afterDate,textSearch]):
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
				queryparams += "content="+quote_plus(textSearch)
			url += queryparams
			Logger.LogMessage('Get -> {}'.format(url))
			response = self.s.get(url) #but wait, discord's gonna be an asshole and only give us the first 25 results, rip heres a loop
			displayedresponse = response.json() #after this...
			if 'messages' in displayedresponse: #if request response not 400
				displayedresponse['messages'] = '...' #cause console space
			if 'total_results' in response.json(): #now onto getting all the messages...note for old/active servers this can be a pain in the ass
				actualresponse = response.json() #youve got to be shitting me
				actualresponse['messages'] = [] #just removing all the shit
				total_pages = math.ceil(response.json()['total_results']/25) #this changes...............
				n=0 #page num
				while n<total_pages:
					time.sleep(waitTime)
					nextpageurl = url + "&offset="+str(n*25)
					Logger.LogMessage('Get -> {}'.format(nextpageurl))
					nextpageresponse = self.s.get(nextpageurl)
					if 'retry_after' in nextpageresponse.json():
						print('rate limited: waiting for '+str(nextpageresponse.json()['retry_after']/1000)+' seconds')
						time.sleep(nextpageresponse.json()['retry_after']/1000 + 1) #add an extra second just in case
						nextpageresponse = self.s.get(nextpageurl) #run that shit again
					total_pages = math.ceil(nextpageresponse.json()['total_results']/25) #update total_pages in case it changed
					Logger.LogMessage('Response <- {}'.format("next 25 messages loaded"), log_level=LogLevel.OK)
					hitresponses = [] # now...discord's shit never ends cause nextpageresponse.json()['messages'] is a list of length something and includes some junk....so we have to get rid of that junk
					for k in range(len(nextpageresponse.json()['messages'])): #for every group
						for j in range(len(nextpageresponse.json()['messages'][k])): #for every item in every group
							if 'hit' in nextpageresponse.json()['messages'][k][j]: #fml
								hitresponses.append(nextpageresponse.json()['messages'][k][j])
								print('1')
								print(nextpageresponse.json()['messages'][k][j]) ####debug line, remove if u want*****
					actualresponse['messages'].extend(hitresponses)
					n+=1 #onto the next page
				actualresponse['messages'] = list({v['id']:v for v in actualresponse['messages']}.values()) #in case duplicates formed, thank u stackexchange
				actualresponse['total_results'] = len(actualresponse['messages']) #update total results num
				return actualresponse
		Logger.LogMessage('Get -> {}'.format(url))
		response = self.s.get(url)
		displayedresponse = response.json()
		if 'messages' in displayedresponse: #if request response not 400
			displayedresponse['messages'] = '...' #cause total results can go well over 10k
		if 'total_results' in response.json(): #now onto getting all the messages...note for old/active servers this can be a pain in the ass
			actualresponse = response.json() #youve got to be shitting me
			actualresponse['messages'] = [] #just removing all the shit
			total_pages = math.ceil(response.json()['total_results']/25) #this changes
			n=0 #page num
			while n<total_pages:
				time.sleep(waitTime)
				nextpageurl = url + "&offset="+str(n*25)
				Logger.LogMessage('Get -> {}'.format(nextpageurl))
				nextpageresponse = self.s.get(nextpageurl)
				if 'retry_after' in nextpageresponse.json():
					print('rate limited: waiting for '+str(nextpageresponse.json()['retry_after']/1000)+' seconds')
					time.sleep(nextpageresponse.json()['retry_after']/1000 + 1) #add an extra second just in case
					nextpageresponse = self.s.get(nextpageurl) #run that shit again
				total_pages = math.ceil(nextpageresponse.json()['total_results']/25) #update total_pages in case it changed
				Logger.LogMessage('Response <- {}'.format("next 25 messages loaded"), log_level=LogLevel.OK)
				hitresponses = [] # now...discord's shit never ends cause nextpageresponse.json()['messages'] is a list of length something and includes some junk....so we have to get rid of that junk
				for k in range(len(nextpageresponse.json()['messages'])): #for every group
					for j in range(len(nextpageresponse.json()['messages'][k])): #for every item in every group
						if 'hit' in nextpageresponse.json()['messages'][k][j]:
							hitresponses.append(nextpageresponse.json()['messages'][k][j])
							print('2')
							print(nextpageresponse.json()['messages'][k][j]) ####debug line, remove if u want*****
				actualresponse['messages'].extend(hitresponses)
				n+=1 #onto the next page
			actualresponse['messages'] = list({v['id']:v for v in actualresponse['messages']}.values()) #in case duplicates formed, thank u stackexchange
			actualresponse['total_results'] = len(actualresponse['messages']) #update total results num
			return actualresponse

	#get recent messages (up to 100)
	def getRecentMessage(self,channelID,num): # num <= 100
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

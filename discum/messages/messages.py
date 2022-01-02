from requests_toolbelt import MultipartEncoder
import random, string
import time, datetime
import os.path
import json
import base64

from ..utils.fileparse import Fileparse
from ..utils.contextproperties import ContextProperties
from ..utils.nonce import calculateNonce
from ..RESTapiwrap import Wrapper

try:
	from urllib.parse import quote_plus, urlparse, urlencode
except ImportError:
	from urllib import quote_plus, urlencode
	from urlparse import urlparse

class Messages(object):
	__slots__ = ['discord', 's', 'log']
	def __init__(self, discord, s, log): #s is the requests session object
		self.discord = discord
		self.s = s
		self.log = log

	#just the raw endpoint
	def createDMraw(self, recipients):
		url = self.discord+"users/@me/channels"
		if isinstance(recipients, str):
			recipients = [recipients]
		body = {"recipients": recipients}
		if len(recipients)>1:
			context = ContextProperties.get("new group dm")
		else:
			context = "e30=" #{}
		return Wrapper.sendRequest(self.s, 'post', url, body, headerModifications={"update":{"X-Context-Properties":context}}, log=self.log)

	#create a DM
	def createDM(self, recipients):
		req = self.createDMraw(recipients)
		self.getMessages(req.json()["id"], num=50, beforeDate=None, aroundMessage=None)
		return req

	#deleteChannel (also works for deleting dms/dm-groups)
	def deleteChannel(self, channelID):
		url = self.discord+'channels/'+channelID
		return Wrapper.sendRequest(self.s, 'delete', url, log=self.log)

	def removeFromDmGroup(self, channelID, userID):
		url = self.discord+'channels/'+channelID+'/recipients/'+userID
		return Wrapper.sendRequest(self.s, 'delete', url, log=self.log)

	def addToDmGroup(self, channelID, userID):
		url = self.discord+'channels/'+channelID+'/recipients/'+userID
		context = ContextProperties.get("add friends to dm")
		return Wrapper.sendRequest(self.s, 'put', url, headerModifications={"update":{"X-Context-Properties":context}}, log=self.log)

	def createDmGroupInvite(self, channelID, max_age_seconds):
		url = self.discord+'channels/'+channelID+'/invites'
		if max_age_seconds == False:
			max_age_seconds = 0
		body = {"max_age": max_age_seconds}
		context = ContextProperties.get("Group DM Invite Create")
		return Wrapper.sendRequest(self.s, 'post', url, body, headerModifications={"update":{"X-Context-Properties":context}}, log=self.log)

	def setDmGroupName(self, channelID, name):
		url = self.discord+'channels/'+channelID
		body = {"name": name}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def setDmGroupIcon(self, channelID, imagePath):
		url = self.discord+'channels/'+channelID
		with open(imagePath, "rb") as image:
			encodedImage = base64.b64encode(image.read()).decode('utf-8')
		body = {"icon":"data:image/png;base64,"+encodedImage}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	#get messages
	def getMessages(self,channelID,num,beforeDate,aroundMessage): # num is between 1 and 100, beforeDate is a snowflake
		url = self.discord+"channels/"+channelID+"/messages?limit="+str(num)
		if beforeDate != None:
			url += "&before="+str(beforeDate)
		elif aroundMessage != None:
			url += "&around="+str(aroundMessage)
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	#get message by channel ID and message ID
	def getMessage(self, channelID, messageID):
		url = self.discord+"channels/"+channelID+"/messages?limit=1&around="+messageID
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	#greet with stickers
	def greet(self, channelID, sticker_ids):
		url = self.discord+"channels/"+channelID+"/greet"
		if isinstance(sticker_ids, str):
			sticker_ids = [sticker_ids]
		body = {"sticker_ids": sticker_ids}
		return Wrapper.sendRequest(self.s, 'post', url, body, log=self.log)

	#text message
	def sendMessage(self, channelID, message, nonce, tts, embed, message_reference, allowed_mentions, sticker_ids):
		url = self.discord+"channels/"+channelID+"/messages"
		body = {"content": message, "tts": tts}
		if nonce == "calculate":
			nonce = calculateNonce()
		else:
			nonce = str(nonce)
		body["nonce"] = nonce
		if embed != None:
			body["embed"] = embed
		if message_reference != None:
			body["message_reference"] = message_reference
		if allowed_mentions != None:
			body["allowed_mentions"] = allowed_mentions
		if sticker_ids != None:
			body["sticker_ids"] = sticker_ids
		return Wrapper.sendRequest(self.s, 'post', url, body, log=self.log)

	#send file
	def sendFile(self,channelID,filelocation,isurl,message, tts, message_reference, sticker_ids):
		mimetype, extensiontype, fd = Fileparse(self.s,self.log).parse(filelocation,isurl) #guess extension from file data
		if mimetype == 'invalid': #error out
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
		
		payload = {"content":message,"tts":tts}
		if message_reference != None:
			payload["message_reference"] = message_reference
			payload["type"] = 19
		if sticker_ids != None:
			payload["sticker_ids"] = sticker_ids
		if not isurl:
			fd = open(filelocation,'rb').read()
		fields={"file":(filename,fd,mimetype), "payload_json":(None,json.dumps(payload))}
		
		randomstr = ''.join(random.sample(string.ascii_letters+string.digits,16))
		m = MultipartEncoder(fields=fields,boundary='----WebKitFormBoundary'+randomstr)
		headerMods = {"update": {"Content-Type":m.content_type}}
		response = Wrapper.sendRequest(self.s, 'post', url, body=m, headerModifications=headerMods, log=self.log)
		return response

	def reply(self, channelID, messageID, message, nonce, tts, embed, allowed_mentions, sticker_ids, file, isurl):
		if file == None:
			self.sendMessage(channelID, message, nonce=nonce, tts=tts, embed=embed, message_reference={"channel_id":channelID,"message_id":messageID}, allowed_mentions=allowed_mentions, sticker_ids=sticker_ids)
		else:
			self.sendFile(channelID, file, isurl=isurl, message=message, tts=tts, message_reference={"channel_id":channelID,"message_id":messageID}, sticker_ids=sticker_ids)

	def searchMessages(self, guildID, channelID, authorID, authorType, mentionsUserID, has, linkHostname, embedProvider, embedType, attachmentExtension, attachmentFilename, mentionsEveryone, includeNsfw, sortBy, sortOrder, afterDate, beforeDate, textSearch, afterNumResults, limit): #classic discord search function, results with key "hit" are the results you searched for, afterNumResults (aka offset) is multiples of 25 and indicates after which messages (type int), filterResults defaults to False
		if guildID:
			url = self.discord+"guilds/"+guildID+"/messages/search?"
		else:
			if isinstance(channelID, str):
				url = self.discord+"channels/{}/messages/search?".format(channelID)
			else:
				url = self.discord+"channels/{}/messages/search?".format(channelID[0])
		allqueryparams = []
		if channelID:
			if isinstance(channelID, str):
				channelID = [channelID]
			for i in channelID:
				allqueryparams.append(("channel_id", str(i)))
		if authorID:
			if isinstance(authorID, str):
				authorID = [authorID]
			for i in authorID:
				allqueryparams.append(("author_id", str(i)))
		if authorType:
			if isinstance(authorType, str):
				authorType = [authorType]
			for i in authorType:
				allqueryparams.append(("author_type", str(i)))
		if mentionsUserID:
			if isinstance(mentionsUserID, str):
				mentionsUserID = [mentionsUserID]
			for i in mentionsUserID:
				allqueryparams.append(("mentions", str(i)))
		if has:
			if isinstance(has, str):
				has = [has]
			for i in has:
				allqueryparams.append(("has", str(i)))
		if linkHostname:
			if isinstance(linkHostname, str):
				linkHostname = [linkHostname]
			for i in linkHostname:
				allqueryparams.append(("link_hostname", str(i)))
		if embedProvider:
			if isinstance(embedProvider, str):
				embedProvider = [embedProvider]
			for i in embedProvider:
				allqueryparams.append(("embed_provider", str(i)))
		if embedType:
			if isinstance(embedType, str):
				embedType = [embedType]
			for i in embedType:
				allqueryparams.append(("embed_type", str(i)))
		if attachmentExtension:
			if isinstance(attachmentExtension, str):
				attachmentExtension = [attachmentExtension]
			for i in attachmentExtension:
				allqueryparams.append(("attachment_extension", str(i)))
		if attachmentFilename:
			if isinstance(attachmentFilename, str):
				attachmentFilename = [attachmentFilename]
			for i in attachmentFilename:
				allqueryparams.append(("attachment_filename", str(i)))
		if mentionsEveryone:
			allqueryparams.append(("mention_everyone", repr(mentionsEveryone).lower()))
		if beforeDate:
			allqueryparams.append(("max_id", str(beforeDate)))
		if afterDate:
			allqueryparams.append(("min_id", str(afterDate)))
		if textSearch:
			allqueryparams.append(("content", str(textSearch)))
		if includeNsfw:
			allqueryparams.append(("include_nsfw", "true"))
		if sortBy:
			allqueryparams.append(("sort_by", sortBy))
		if sortOrder:
			allqueryparams.append(("sort_order", sortOrder))
		if afterNumResults:
			allqueryparams.append(("offset", str(afterNumResults)))
		if limit!=None:
			allqueryparams.append(("limit", str(limit)))
		querystring = urlencode(allqueryparams)
		url += querystring
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	def filterSearchResults(self, searchResponse): #only input is the requests response object or the dictionary response
		if hasattr(searchResponse, 'json'):
			jsonresponse = searchResponse.json()['messages']
		else:
			jsonresponse = searchResponse
		filteredMessages = []
		for group in jsonresponse:
			for result in group:
				if 'hit' in result:
					filteredMessages.append(result)
		return filteredMessages

	def typingAction(self, channelID): #sends the typing action for 10 seconds (or until you change the page)
		url = self.discord+"channels/"+channelID+"/typing"
		return Wrapper.sendRequest(self.s, 'post', url, log=self.log)

	def editMessage(self, channelID, messageID, newMessage, newEmbed):
		url = self.discord+"channels/"+channelID+"/messages/"+messageID
		body = {"content": newMessage}
		if newEmbed != None:
			body["embed"] = newEmbed
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def deleteMessage(self, channelID, messageID):
		url = self.discord+"channels/"+channelID+"/messages/"+messageID
		return Wrapper.sendRequest(self.s, 'delete', url, log=self.log)

	def pinMessage(self, channelID, messageID):
		url = self.discord+"channels/"+channelID+"/pins/"+messageID
		return Wrapper.sendRequest(self.s, 'put', url, log=self.log)

	def unPinMessage(self, channelID, messageID):
		url = self.discord+"channels/"+channelID+"/pins/"+messageID
		return Wrapper.sendRequest(self.s, 'delete', url, log=self.log)

	def getPins(self, channelID): #get pinned messages
		url = self.discord+"channels/"+channelID+"/pins"
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	def addReaction(self, channelID, messageID, emoji):
		parsedEmoji = quote_plus(emoji)
		url = self.discord+"channels/"+channelID+"/messages/"+messageID+"/reactions/"+parsedEmoji+"/%40me"
		return Wrapper.sendRequest(self.s, 'put', url, log=self.log)

	def removeReaction(self, channelID, messageID, emoji):
		parsedEmoji = quote_plus(emoji)
		url = self.discord+"channels/"+channelID+"/messages/"+messageID+"/reactions/"+parsedEmoji+"/%40me"
		return Wrapper.sendRequest(self.s, 'delete', url, log=self.log)

	def getReactionUsers(self,channelID,messageID,emoji,afterUserID,limit):
		parsedEmoji = quote_plus(emoji)
		url = self.discord+"channels/"+channelID+"/messages/"+messageID+"/reactions/"+parsedEmoji+"?limit="+str(limit)
		if afterUserID:
			url += '&after='+str(afterUserID)
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	#acknowledge message (mark message read)
	def ackMessage(self, channelID, messageID, ackToken):
		url = self.discord+"channels/"+channelID+"/messages/"+messageID+"/ack"
		body = {"token": ackToken}
		return Wrapper.sendRequest(self.s, 'post', url, body, log=self.log)

	#unacknowledge message (mark message unread)
	def unAckMessage(self, channelID, messageID, numMentions):
		url = self.discord+"channels/"+channelID+"/messages/"+messageID+"/ack"
		body = {"manual": True, "mention_count": numMentions}
		return Wrapper.sendRequest(self.s, 'post', url, body, log=self.log)

	def bulkAck(self, data):
		url = self.discord+"read-states/ack-bulk"
		body = {"read_states": data}
		return Wrapper.sendRequest(self.s, 'post', url, body, log=self.log)

	def getTrendingGifs(self, provider, locale, media_format):
		url = self.discord+"gifs/trending?provider="+provider+"&locale="+locale+"&media_format="+media_format
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

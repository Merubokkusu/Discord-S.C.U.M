from ..fileparse.fileparse import Fileparse
from requests_toolbelt import MultipartEncoder
import random,string
import os.path
import time, datetime
import json
from ..RESTapiwrap import *

if __import__('sys').version.split(' ')[0] < '3.0.0':
    from urllib import quote_plus
    from urlparse import urlparse
else:
    from urllib.parse import quote_plus, urlparse

class Messages(object):
    def __init__(self, discord, s, log): #s is the requests session object
        self.discord = discord
        self.s = s
        self.log = log

    def calculateNonce(self, date="now"):
        if date == "now":
            date = datetime.datetime.now()
        unixts = time.mktime(date.timetuple())
        return str((int(unixts)*1000-1420070400000)*4194304)

    #add DM
    def createDM(self,recipients):
        url = self.discord+"users/@me/channels"
        body = {"recipients": recipients}
        return Wrapper.sendRequest(self.s, 'post', url, body, log=self.log)

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

    #text message
    def sendMessage(self, channelID, message, nonce, tts=False, embed=None, message_reference=None, allowed_mentions=None, sticker_ids=None):
        url = self.discord+"channels/"+channelID+"/messages"
        if nonce == "calculate":
            body = {"content": message, "tts": tts, "nonce": self.calculateNonce()}
        else:
            body = {"content": message, "tts": tts, "nonce": str(nonce)}
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
    def sendFile(self,channelID,filelocation,isurl=False,message="", tts=False, message_reference=None, sticker_ids=None):
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
        if isurl:
            payload = {"content":message,"tts":tts}
            if message_reference != None:
                payload["message_reference"] = message_reference
                payload["type"] = 19
            if sticker_ids != None:
                payload["sticker_ids"] = sticker_ids
            fields={"file":(filename,fd,mimetype), "payload_json":(None,json.dumps(payload))}
        else:
            payload = {"content":message,"tts":tts}
            if message_reference != None:
                payload["message_reference"] = message_reference
                payload["type"] = 19
            if sticker_ids != None:
                payload["sticker_ids"] = sticker_ids
            fields={"file":(filename,open(filelocation,'rb').read(),mimetype), "payload_json":(None,json.dumps(payload))}
        m=MultipartEncoder(fields=fields,boundary='----WebKitFormBoundary'+''.join(random.sample(string.ascii_letters+string.digits,16)))
        self.s.headers.update({"Content-Type":m.content_type})
        response = Wrapper.sendRequest(self.s, 'post', url, body=m, log=self.log)
        self.s.headers.update({"Content-Type":"application/json"})
        return response

    def reply(self, channelID, messageID, message, nonce, tts=False, embed=None, allowed_mentions={"parse":["users","roles","everyone"],"replied_user":False}, sticker_ids=None, file=None, isurl=False):
        if file == None:
            self.sendMessage(channelID, message, nonce=nonce, tts=tts, embed=embed, message_reference={"channel_id":channelID,"message_id":messageID}, allowed_mentions=allowed_mentions, sticker_ids=sticker_ids)
        else:
            self.sendFile(channelID, file, isurl=isurl, message=message, tts=tts, message_reference={"channel_id":channelID,"message_id":messageID}, sticker_ids=sticker_ids)

    def searchMessages(self,guildID,channelID,userID,mentionsUserID,has,beforeDate,afterDate,textSearch,afterNumResults): #classic discord search function, results with key "hit" are the results you searched for, afterNumResults (aka offset) is multiples of 25 and indicates after which messages (type int), filterResults defaults to False
        url = self.discord+"guilds/"+guildID+"/messages/search?"
        queryparams = ""
        if any(v != None for v in [channelID,userID,mentionsUserID,has,beforeDate,afterDate,textSearch,afterNumResults]):
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
                queryparams += "max_id="+str(beforeDate)+"&"
            if afterDate != None and isinstance(afterDate,int):
                queryparams += "min_id="+str(afterDate)+"&"
            if textSearch != None and isinstance(textSearch,str):
                queryparams += "content="+quote_plus(textSearch)+"&"
            if afterNumResults != None and isinstance(afterNumResults,int):
                queryparams += "offset="+str(afterNumResults)
            url += queryparams
        return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

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
        return Wrapper.sendRequest(self.s, 'post', url, log=self.log)

    def editMessage(self,channelID,messageID,newMessage):
        url = self.discord+"channels/"+channelID+"/messages/"+messageID
        body = {"content": newMessage}
        return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

    def deleteMessage(self,channelID,messageID):
        url = self.discord+"channels/"+channelID+"/messages/"+messageID
        return Wrapper.sendRequest(self.s, 'delete', url, log=self.log)

    def pinMessage(self,channelID,messageID):
        url = self.discord+"channels/"+channelID+"/pins/"+messageID
        return Wrapper.sendRequest(self.s, 'put', url, log=self.log)

    def unPinMessage(self,channelID,messageID):
        url = self.discord+"channels/"+channelID+"/pins/"+messageID
        return Wrapper.sendRequest(self.s, 'delete', url, log=self.log)

    def getPins(self,channelID): #get pinned messages
        url = self.discord+"channels/"+channelID+"/pins"
        return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

    def addReaction(self,channelID,messageID,emoji):
        parsedEmoji = quote_plus(emoji)
        url = self.discord+"channels/"+channelID+"/messages/"+messageID+"/reactions/"+parsedEmoji+"/%40me"
        return Wrapper.sendRequest(self.s, 'put', url, log=self.log)

    def removeReaction(self,channelID,messageID,emoji):
        parsedEmoji = quote_plus(emoji)
        url = self.discord+"channels/"+channelID+"/messages/"+messageID+"/reactions/"+parsedEmoji+"/%40me"
        return Wrapper.sendRequest(self.s, 'delete', url, log=self.log)

    #acknowledge message (mark message read)
    def ackMessage(self,channelID,messageID,ackToken):
        url = self.discord+"channels/"+channelID+"/messages/"+messageID+"/ack"
        body = {"token": ackToken}
        return Wrapper.sendRequest(self.s, 'post', url, body, log=self.log)

    #unacknowledge message (mark message unread)
    def unAckMessage(self,channelID,messageID,numMentions):
        url = self.discord+"channels/"+channelID+"/messages/"+messageID+"/ack"
        body = {"manual": True, "mention_count": numMentions}
        return Wrapper.sendRequest(self.s, 'post', url, body, log=self.log)

    def bulkAck(self, data):
        url = self.discord+"read-states/ack-bulk"
        body = {"read_states": data}
        return Wrapper.sendRequest(self.s, 'post', url, body, log=self.log)

    def getTrendingGifs(self, provider="tenor", locale="en-US", media_format="mp4"):
        url = self.discord+"gifs/trending?provider="+provider+"&locale="+locale+"&media_format="+media_format
        return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

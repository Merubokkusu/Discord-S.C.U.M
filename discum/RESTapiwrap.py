import copy #only used if header modification is used
import json
import inspect
import brotli #just in case

def brdecompress(payload):
	try:
		data = brotli.decompress(payload)
		return data
	except:
		return payload

def editedReqSession(reqsession, headerModifications):
	editedSession = copy.deepcopy(reqsession)
	if "add" in headerModifications:
		editedSession.headers.update(headerModifications["update"])
	if "remove" in headerModifications:
		for header in headerModifications["remove"]:
			if header in editedSession.headers:
				del editedSession.headers[header]
	return editedSession

class LogLevel:
	INFO = '\033[94m'
	OK = '\033[92m'
	WARNING = '\033[93m'
	DEFAULT = '\033[m'

#The wrap that all http request api functions in discum use
class Wrapper:
	@staticmethod
	def sendRequest(reqsession, method, url, body=None, files=None, headerModifications={}, timeout=None, log=True): #headerModifications = {"add":{}, "remove":[]}
		if hasattr(reqsession, method): #just checks if post, get, whatever is a valid requests method
			stack = inspect.stack()
			function_name = "({}->{})".format(str(stack[1][0].f_locals['self']).split(' ')[0], stack[1][3])
			if log: #(sent) log msg, method and url
				sentMsg = '{} -> {}'.format(method.title(), url)
				print('{} [+] {} {}'.format(LogLevel.INFO, function_name, sentMsg))
				print(LogLevel.DEFAULT)
			data = {} #now onto the body (if exists)
			if body != None:
				if isinstance(body, dict):
					data = {'data': json.dumps(body)}
				else:
					data = {'data': body}
				if log:
					bodyMsg = str(body)
					print('{} [+] {} {}'.format(LogLevel.INFO, function_name, bodyMsg))
					print(LogLevel.DEFAULT)
			if files != None: #files...this isnt actually used yet in discum
				data['files'] = files
				if log:
					print('{} [+] {} {}'.format(LogLevel.INFO, function_name, "<file data>"))
					print(LogLevel.DEFAULT)
			prepReqSession = reqsession
			if headerModifications not in ({}, None): #header modifications, like endpoints that don't need auth or superproperties or stuff like that
				prepReqSession = editedReqSession(prepReqSession, headerModifications)
			if timeout == None:
				response = getattr(prepReqSession, method)(url=url, **data) #where the actual request happens
			else:
				data['timeout'] = timeout
				try:
					response = getattr(prepReqSession, method)(url=url, **data)
					return
				except:
					return
			if response.headers.get('Content-Encoding') == "br": #decompression; gzip/deflate is automatically handled by requests module
				response._content = brdecompress(response.content)
			if log: #(received) log message, response
				receivedMsg = 'Response <- {}'.format(response.text)
				print('{} [+] {} {}'.format(LogLevel.OK, function_name, receivedMsg))
				print(LogLevel.DEFAULT)
			return response
		else:
			print('Invalid request method.')

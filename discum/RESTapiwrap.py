import copy #only used if header modification is used
import json
import inspect
from requests.exceptions import ConnectionError

#functions for REST requests

class LogLevel:
	INFO = '\033[94m'
	OK = '\033[92m'
	WARNING = '\033[93m'
	DEFAULT = '\033[m'

class Wrapper:
	@staticmethod
	def logger(function, data, part):
		if part=="url":
			print('{} [+] {} {}'.format(LogLevel.INFO, function, data))
		elif part=="body":
			print('{} [+] {} {}'.format(LogLevel.INFO, function, data))
		elif part=="response":
			print('{} [+] {} {}'.format(LogLevel.OK, function, data))
		print(LogLevel.DEFAULT)

	@staticmethod
	def brdecompress(payload):
		try:
			import brotli
			data = brotli.decompress(payload)
			return data
		except:
			return payload

	@staticmethod
	def editedReqSession(reqsession, headerModifications): #header modifications, like endpoints that don't need auth or superproperties or stuff like that
		if headerModifications not in ({}, None):
			editedSession = copy.deepcopy(reqsession)
			if "add" in headerModifications:
				editedSession.headers.update(headerModifications["add"])
			if "remove" in headerModifications:
				for header in headerModifications["remove"]:
					if header in editedSession.headers:
						del editedSession.headers[header]
			return editedSession
		else:
			return reqsession

	@staticmethod
	def retryLogic(reqMethod, url, data, log): #only for "Connection reset by peer" errors. Influenced by praw's retry stuff
		remaining_attempts = 3
		while True:
			try:
				return reqMethod(url=url, **data)
			except ConnectionError:
				if log:
					print("Connection reset by peer. Retrying...")
				remaining_attempts -= 1
				if remaining_attempts == 0:
					raise

	@staticmethod
	def sendRequest(reqsession, method, url, body=None, headerModifications={}, timeout=None, log=True): #headerModifications = {"add":{}, "remove":[]}
		if hasattr(reqsession, method): #just checks if post, get, whatever is a valid requests method
			stack = inspect.stack()
			function_name = "({}->{})".format(str(stack[1][0].f_locals['self']).split(' ')[0], stack[1][3])
			reqsession = Wrapper.editedReqSession(reqsession, headerModifications)
			if log: #(sent) log msg, method and url
				sentMsg = '{} -> {}'.format(method.title(), url)
				Wrapper.logger(function_name, sentMsg, part="url")
			data = {} #now onto the body (if exists)
			if body != None:
				if isinstance(body, dict):
					data = {'data': json.dumps(body)}
				else:
					data = {'data': body}
				if log:
					bodyMsg = str(body)
					Wrapper.logger(function_name, bodyMsg, part="body")
			#####
			if timeout != None:
				data['timeout'] = timeout
			response = Wrapper.retryLogic(getattr(reqsession, method), url, data, log)
			#####
			if response.headers.get('Content-Encoding') == "br": #decompression; gzip/deflate is automatically handled by requests module
				response._content = Wrapper.brdecompress(response.content)
			if log: #(received) log message, response
				receivedMsg = 'Response <- {}'.format(response.text)
				Wrapper.logger(function_name, receivedMsg, part="response")
			return response
		else:
			print('Invalid request method.')

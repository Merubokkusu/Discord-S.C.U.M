import copy #only used if header modification is used
import json
import inspect
import time
from requests.exceptions import ConnectionError
from .logger import * #imports LogLevel and Logger

#functions for REST requests in Wrapper class
class Wrapper:
	#returns formatted log string and color for REST requests
	@staticmethod
	def logFormatter(function, data, part):
		# [+] (<class->function) Method -> url
		if part == "url":
			text = "{} -> {}".format(data[0].title(), data[1])
			color = LogLevel.SEND
		# [+] (<class->function) body
		elif part == "body":
			text = str(data)
			color = LogLevel.SEND
		# [+] (<class->function) Response <- response.text
		elif part == "response":
			text = "Response <- {}".format(data)
			color = LogLevel.RECEIVE
		formatted = " [+] {} {}".format(function, text)
		return formatted, color

	#decompression for brotli
	@staticmethod
	def brdecompress(payload, log):
		try:
			import brotli
			data = brotli.decompress(payload)
			return data
		except Exception:
			Logger.log("Either brotli decompress failed or discord returned incorrect content encodings.", None, log) #yea, it happens :/
			return payload

	#header modifications, like endpoints that don't need auth, superproperties, etc; also for updating headers like xfingerprint
	@staticmethod
	def editedReqSession(reqsession, headerModifications):
		if headerModifications not in ({}, None):
			editedSession = copy.deepcopy(reqsession)
			if "update" in headerModifications:
				editedSession.headers.update(headerModifications["update"])
			if "remove" in headerModifications:
				for header in headerModifications["remove"]:
					if header in editedSession.headers:
						del editedSession.headers[header]
			return editedSession
		else:
			return reqsession

	#only for "Connection reset by peer" errors. Influenced by praw's retry code
	@staticmethod
	def retryLogic(reqMethod, url, data, log):
		remaining_attempts = 3
		while True:
			try:
				return reqMethod(url=url, **data)
			except ConnectionError:
				if log:
					Logger.log("Connection reset by peer. Retrying...", None, log)
					time.sleep(0.3)
				remaining_attempts -= 1
				if remaining_attempts == 0:
					break
			except Exception:
				break
		return None

	@staticmethod
	def sendRequest(reqsession, method, url, body=None, headerModifications={}, timeout=None, log={"console":True, "file":False}): #headerModifications = {"update":{}, "remove":[]}
		if hasattr(reqsession, method): #just checks if post, get, whatever is a valid requests method
			# 1. find function
			stack = inspect.stack()
			function_name = "({}->{})".format(str(stack[1][0].f_locals['self']).split(' ')[0], stack[1][3])
			# 2. edit request session if needed
			reqsession = Wrapper.editedReqSession(reqsession, headerModifications)
			# 3. log url
			text, color = Wrapper.logFormatter(function_name, [method, url], part="url")
			Logger.log(text, color, log)
			# 4. format body and log
			data = {} #now onto the body (if exists)
			if body != None:
				if isinstance(body, dict):
					data = {'data': json.dumps(body)}
				else:
					data = {'data': body}
				if log:
					text, color = Wrapper.logFormatter(function_name, body, part="body")
					Logger.log(text, color, log)
			# 5. put timeout in data if needed (when we don't want to wait for a response from discord)
			if timeout != None:
				data['timeout'] = timeout
			# 6. the request
			response = Wrapper.retryLogic(getattr(reqsession, method), url, data, log)
			# 7. brotli decompression of response
			if response and response.headers.get('Content-Encoding') == "br": #decompression; gzip/deflate is automatically handled by requests module
				response._content = Wrapper.brdecompress(response.content, log)
			# 8. log response
			text, color = Wrapper.logFormatter(function_name, response.text, part="response")
			Logger.log(text, color, log)
			# 9. return response object with decompressed content
			return response
		else:
			Logger.log('Invalid request method.', None, log)

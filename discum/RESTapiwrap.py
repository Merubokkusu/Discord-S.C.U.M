import json
import inspect

class LogLevel:
	INFO = '\033[94m'
	OK = '\033[92m'
	WARNING = '\033[93m'
	DEFAULT = '\033[m'

#The wrap that all http request api functions in discum use
class Wrapper:
	@staticmethod
	def sendRequest(reqsession, method, url, body=None, log=True):
		if hasattr(reqsession, method):
			stack = inspect.stack()
			function_name = "({}->{})".format(str(stack[1][0].f_locals['self']).split(' ')[0], stack[1][3])
			if log: #(sent) log msg
				sentMsg = '{} -> {}'.format(method.title(), url)
				print('{} [+] {} {}'.format(LogLevel.INFO, function_name, sentMsg))
				print(LogLevel.DEFAULT)
			if body != None:
				if isinstance(body, dict):
					data = {'data': json.dumps(body)}
				else:
					data = {'data': body}
				if log:
					bodyMsg = '{}'.format(str(body))
					print('{} [+] {} {}'.format(LogLevel.INFO, function_name, bodyMsg))
					print(LogLevel.DEFAULT)
				response = getattr(reqsession, method)(url=url, **data)
			else:
				response = getattr(reqsession, method)(url=url)
			if log: #(received) log message
				receivedMsg = 'Response <- {}'.format(response.text)
				print('{} [+] {} {}'.format(LogLevel.OK, function_name, receivedMsg))
				print(LogLevel.DEFAULT)
			return response
		else:
			print('Invalid request method.')

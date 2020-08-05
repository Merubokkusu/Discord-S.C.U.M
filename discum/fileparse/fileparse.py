import filetype
from urllib.parse import urlparse
import requests
import os

class Fileparse(object):
	def __init__(self, s): #s is the requests session object
		self.s = s
		
	def parse(self, filelocation, isurl): #returns mimetype and extension if detected
		fd = b""
		if isurl:
			result = urlparse(filelocation)
			if all([result.scheme, result.netloc, result.path]): #if a link...
				fd = requests.get(filelocation,headers={"User-Agent":self.s.headers['User-Agent']},proxies=self.s.proxies).content
				kind = filetype.guess(fd)
				if kind is None:
					print('Unsupported file type. Will attempt to send anyways.')
					return 'unsupported', 'unsupported', fd
				return kind.mime, kind.extension, fd
			else:
				print('Invalid link.')
				return 'invalid', 'invalid', fd
		else:
			if os.path.isfile(filelocation):
				kind = filetype.guess(filelocation)
				if kind is None:
					print('Unsupported file type. Will attempt to send anyways.')
					return 'unsupported', 'unsupported', fd
				return kind.mime, kind.extension, fd
			else:
				print('Either not a file or file does not exist.')
				return 'invalid', 'invalid', fd

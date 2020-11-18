import filetype
import requests
import os

if __import__('sys').version.split(' ')[0] < '3.0.0':
    from urlparse import urlparse
else:
    from urllib.parse import urlparse

class Fileparse(object):
	def __init__(self, s, log): #s is the requests session object
		self.s = s
		self.log = log
		
	def parse(self, filelocation, isurl): #returns mimetype and extension if detected
		fd = b""
		if isurl:
			result = urlparse(filelocation)
			if all([result.scheme, result.netloc, result.path]): #if a link...
				fd = requests.get(filelocation,headers={"User-Agent":self.s.headers['User-Agent']},proxies=self.s.proxies).content
				kind = filetype.guess(fd)
				if kind is None:
					if self.log: print('Unsupported file type. Will attempt to send anyways.')
					return 'unsupported', 'unsupported', fd
				return kind.mime, kind.extension, fd
			else:
				if self.log: print('Invalid link.')
				return 'invalid', 'invalid', fd
		else:
			if os.path.isfile(filelocation):
				kind = filetype.guess(filelocation)
				if kind is None:
					if self.log: print('Unsupported file type. Will attempt to send anyways.')
					return 'unsupported', 'unsupported', fd
				return kind.mime, kind.extension, fd
			else:
				if self.log: print('Either not a file or file does not exist.')
				return 'invalid', 'invalid', fd

import filetype
import requests
import os

from ..logger import * #imports LogLevel and Logger

try:
    from urlparse import urlparse
except ImportError:
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
					Logger.log('Unsupported file type. Will attempt to send anyways.', LogLevel.WARNING, self.log)
					return 'unsupported', 'unsupported', fd
				return kind.mime, kind.extension, fd
			else:
				Logger.log('Invalid link.', LogLevel.WARNING, self.log)
				return 'invalid', 'invalid', fd
		else:
			if os.path.isfile(filelocation):
				kind = filetype.guess(filelocation)
				if kind is None:
					Logger.log('Unsupported file type. Will attempt to send anyways.', LogLevel.WARNING, self.log)
					return 'unsupported', 'unsupported', fd
				return kind.mime, kind.extension, fd
			else:
				Logger.log('Either not a file or file does not exist.', LogLevel.WARNING, self.log)
				return 'invalid', 'invalid', fd

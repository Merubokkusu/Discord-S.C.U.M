import filetype
from urllib.parse import urlparse
from urllib.request import Request, urlopen
import os

class Fileparse(object):
	def parse(self, filelocation, isurl): #returns mimetype and extension if detected
		if isurl:
			result = urlparse(filelocation)
			if all([result.scheme, result.netloc, result.path]): #if a link...
				req = Request(filelocation, headers={'User-Agent': 'Mozilla/5.0'})
				fd = urlopen(req).read()
				kind = filetype.guess(fd)
				if kind is None:
					print('Unsupported file type. Will attempt to send anyways.')
					return 'unsupported', 'unsupported'
				return kind.mime, kind.extension
			else:
				print('Invalid link.')
				return 'invalid', 'invalid'
		else:
			if os.path.isfile(filelocation):
				kind = filetype.guess(filelocation)
				if kind is None:
					print('Unsupported file type. Will attempt to send anyways.')
					return 'unsupported', 'unsupported'
				return kind.mime, kind.extension
			else:
				print('Either not a file or file does not exist.')
				return 'invalid', 'invalid'

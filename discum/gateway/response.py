#structure of the Resp object (Resp is short for response)
'''
resp = Resp(response)
resp.raw        #returns raw (dict, decompressed) response from gateway
resp.event...   #handles event checking (resp.event.ready will be True if the response is of type READY)
resp.parsed...  #handles automatically parsing responses, has specific functions for specific types of responses (messages are handled differently from guild member list updates)
                #also has the ability to update bot objects like session
'''

from .event import Event
from .parse import Parse

class Resp:
	def __init__(self, response):
		self.raw = response
		self.event = Event(response)
		self.parsed = Parse(response)
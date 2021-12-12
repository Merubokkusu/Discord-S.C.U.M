from ..RESTapiwrap import Wrapper
import time, datetime
import random

from ..utils.client_uuid import Client_UUID

class Science(object):
	__slots__ = ['discord', 's', 'log', 'analytics_token', 'UUIDobj']
	def __init__(self, discord, s, log, analytics_token, userID): #s is the requests session object
		self.discord = discord
		self.s = s
		self.log = log
		self.analytics_token = analytics_token
		if userID == "0":
			date = datetime.datetime.now()
			unixts = time.mktime(date.timetuple())
			userID = str((int(unixts)*1000-1420070400000)*4194304)
		self.UUIDobj = Client_UUID(userID)

	def getCurrentUnixMS(self): #returns unix ts in milliseconds
		return int(time.mktime(datetime.datetime.now().timetuple()) * 1000)

	def getTrackingProperties(self, duration="random"):
		now = self.getCurrentUnixMS()
		trackingProperties = {"client_track_timestamp": now}
		if duration == "random":
			trackingProperties["client_send_timestamp"] = now+random.randint(40, 1000)
		else:
			trackingProperties["client_send_timestamp"] = now+duration
		trackingProperties["client_uuid"] = self.UUIDobj.calculate(eventNum="default", userID="default", increment=True)
		return trackingProperties

	def science(self, events): #https://luna.gitlab.io/discord-unofficial-docs/science_events.html
		url = self.discord +"science"
		for event in events:
			if "type" not in event:
				event["type"] = "keyboard_mode_toggled" #random default type
			if "properties" not in event or "client_send_timestamp" not in event["properties"] or "client_track_timestamp" not in event["properties"] or "client_uuid" not in event["properties"]:
				event["properties"] = self.getTrackingProperties()
			else:
				self.UUIDobj.eventNum += 1
		body = {'token': self.analytics_token, 'events':events}
		if self.analytics_token == None: #if not logged in. ex: bot=discum.Client(token='poop')
			headerModifications = {"remove": ["Authorization"]}
			return Wrapper.sendRequest(self.s, 'post', url, body, headerModifications=headerModifications, log=self.log)
		else:
			return Wrapper.sendRequest(self.s, 'post', url, body, log=self.log)

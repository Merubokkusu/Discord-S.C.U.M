from ..RESTapiwrap import *
import time, datetime
import random

from .client_uuid import Client_UUID

class Science(object):
    def __init__(self, discord, s, log, analytics_token, userID, xfingerprint): #s is the requests session object
        self.discord = discord
        self.s = s
        self.log = log
        self.analytics_token = analytics_token
        self.xfingerprint = xfingerprint
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
        trackingProperties["client_uuid"] = self.UUIDobj.calculate()
        return trackingProperties

    def science(self, events): #https://luna.gitlab.io/discord-unofficial-docs/science_events.html
        url = self.discord +"science"
        for event in events:
            if "type" not in event:
                event["type"] = "keyboard_shortcut_used" #random default type, will make an event helper later
            if "properties" not in event or "client_send_timestamp" not in event["properties"] or "client_track_timestamp" not in event["properties"] or "client_uuid" not in event["properties"]:
                event["properties"] = self.getTrackingProperties()
            else:
                self.UUIDobj.eventNum += 1
        body = {'token': self.analytics_token, 'events':events}
        if self.analytics_token == None: #if not logged in. ex: bot=discum.Client(token='poop')
            body.pop('token')
            import requests
            s = requests.Session()
            s.proxies.update(self.s.proxies)
            for header in self.s.headers:
                if header != "Authorization":
                    s.headers[header] = self.s.headers[header]
                else:
                    s.headers["Authorization"] = None
                    s.headers["X-fingerprint"] = self.xfingerprint
        else:
            s = self.s
        return Wrapper.sendRequest(s, 'post', url, body, log=self.log)
#combo
import time, datetime
class UserCombo(object):
	__slots__ = ['gatewayobj']
	def __init__(self, gatewayobj):
		self.gatewayobj = gatewayobj

	def getCurrentUnixTs(self):
		date = datetime.datetime.now()
		unixts = int(time.mktime(date.timetuple())*1000) #milliseconds
		return unixts

	def constructEmojiDict(self, emoji, animatedEmoji):
		if emoji != None:
			if ":" in emoji:
				name, ID = emoji.split(":")
			else:
				name = emoji
				ID = None
			emojiDict = {}
			emojiDict.update({"id": ID, "name": name, "animated": animatedEmoji})
		else: #None
			emojiDict = None
		return emojiDict

	def constructActivitiesList(self, updates={}, remove=None): #update is a bit too raw, will fix later
		currentActivities = self.gatewayobj.session.userSettings["activities"]		
		activities = {4: {}, 0: {}, 1: {}, 2: {}, 3: {}}
		for i in currentActivities: #all this does is fix the format of current activities
			if remove!=i: #this helps remove activities
				activities[i] = dict(currentActivities[i])
				activities[i].pop("created_at", None)
				activities[i].pop("id", None)
				if "emoji" in activities[i]:
					if activities[i]["emoji"]!=None:
						emojiState = dict(currentActivities[i]["emoji"])
						name = emojiState.pop("name", "")
						ID = emojiState.pop("id", None)
						emojiStr = name+":"+ID if ID!=None else name
						animatedEmoji = emojiState.pop("animated", False)
					else:
						emojiStr = None
						animatedEmoji = False
					activities[i]["emoji"] = self.constructEmojiDict(emojiStr, animatedEmoji)
		for i in updates: #this adds activities
			activities[i] = updates[i]
		activitiesList = [activities[j] for j in activities if len(activities[j])>0]
		return activitiesList

	def setStatus(self, status):
		if status != self.gatewayobj.session.userSettings["status"]:
			self.gatewayobj.request.setStatus(status, self.constructActivitiesList())

	def setPlayingStatus(self, game): #will add metadata later
		currentStatus = self.gatewayobj.session.userSettings["status"]
		updates = {
		    0: {
		        "type": 0,
		        "name": game,
		        "timestamps": {"start": self.getCurrentUnixTs()}
		    }
		}
		self.gatewayobj.request.setStatus(currentStatus, self.constructActivitiesList(updates=updates))

	def removePlayingStatus(self):
		currentStatus = self.gatewayobj.session.userSettings["status"]
		self.gatewayobj.request.setStatus(currentStatus, self.constructActivitiesList(remove=0))

	def setStreamingStatus(self, stream, url): #will add metadata later
		currentStatus = self.gatewayobj.session.userSettings["status"]
		updates = {
		    1: {
		        "type": 1,
		        "name": stream,
		        "url": url,
		        "timestamps": {"start": self.getCurrentUnixTs()}
		    }
		}
		self.gatewayobj.request.setStatus(currentStatus, self.constructActivitiesList(updates=updates))

	def removeStreamingStatus(self): 
		currentStatus = self.gatewayobj.session.userSettings["status"]
		self.gatewayobj.request.setStatus(currentStatus, self.constructActivitiesList(remove=1))

	def setListeningStatus(self, song): #will add metadata later
		currentStatus = self.gatewayobj.session.userSettings["status"]
		updates = {
		    2: {
		        "type": 2,
		        "name": song,
		        "timestamps": {"start": self.getCurrentUnixTs()}
		    }
		}
		self.gatewayobj.request.setStatus(currentStatus, self.constructActivitiesList(updates=updates))

	def removeListeningStatus(self):
		currentStatus = self.gatewayobj.session.userSettings["status"]
		self.gatewayobj.request.setStatus(currentStatus, self.constructActivitiesList(remove=2))

	def setWatchingStatus(self, show): #will add metadata later
		currentStatus = self.gatewayobj.session.userSettings["status"]
		updates = {
		    3: {
		        "type": 3,
		        "name": show,
		        "timestamps": {"start": self.getCurrentUnixTs()}
		    }
		}
		self.gatewayobj.request.setStatus(currentStatus, self.constructActivitiesList(updates=updates))

	def removeWatchingStatus(self):
		currentStatus = self.gatewayobj.session.userSettings["status"]
		self.gatewayobj.request.setStatus(currentStatus, self.constructActivitiesList(remove=3))

	def setCustomStatus(self, customstatus, emoji, animatedEmoji):
		currentStatus = self.gatewayobj.session.userSettings["status"]
		updates = {
		    4: {
		        "type": 4,
		        "state": customstatus,
		        "name": "Custom Status",
		        "emoji": self.constructEmojiDict(emoji, animatedEmoji),
		    }
		}
		self.gatewayobj.request.setStatus(currentStatus, self.constructActivitiesList(updates=updates))

	def removeCustomStatus(self):
		currentStatus = self.gatewayobj.session.userSettings["status"]
		self.gatewayobj.request.setStatus(currentStatus, self.constructActivitiesList(remove=4))

	def clearActivities(self):
		currentStatus = self.gatewayobj.session.userSettings["status"]
		self.gatewayobj.request.setStatus(currentStatus, [])

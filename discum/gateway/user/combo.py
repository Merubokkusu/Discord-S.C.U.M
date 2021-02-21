#combo
import datetime #eh will need this later

class UserCombo(object):
	def __init__(self, gatewayobj):
		self.gatewayobj = gatewayobj

	def constructActivitiesList(self, updates={}, remove=None): #update is a bit too raw, will fix later
		currentActivities = self.gatewayobj.session.userSettings["activities"]		
		activities = {4: {}, 0: {}, 1: {}, 2: {}, 3: {}}
		for i in currentActivities:
			if i==4 and remove!=i:
				activities[4]["type"] = 4
				activities[4]["state"] = currentActivities[4]["state"]
				activities[4]["name"] = "Custom Status"
				activities[4]["emoji"] = None #idk will fix later
			elif remove!=i: #idk will fix later
				activities[i]["type"] = i
				activities[i]["name"] = currentActivities[i]["name"]
				activities[i]["timestamps"] = currentActivities[i]["timestamps"]
		activities.update(updates)
		activitiesList = []
		for j in activities:
			if len(activities[j])>0:
				activitiesList.append(activities[j])
		return activitiesList

	def setStatus(self, status):
		if status != self.gatewayobj.session.userSettings["status"]:
			self.gatewayobj.request.setStatus(status, self.constructActivitiesList())

	#def setPlayingStatus(self, game):

	def removePlayingStatus(self):
		currentStatus = self.gatewayobj.session.userSettings["status"]
		self.gatewayobj.request.setStatus(currentStatus, self.constructActivitiesList(remove=0))

	#def setStreamingStatus(self, stream, metadata={}): 

	def removeStreamingStatus(self):
		currentStatus = self.gatewayobj.session.userSettings["status"]
		self.gatewayobj.request.setStatus(currentStatus, self.constructActivitiesList(remove=1))

	#def setListeningStatus(self, song, metadata={}): 

	def removeListeningStatus(self):
		currentStatus = self.gatewayobj.session.userSettings["status"]
		self.gatewayobj.request.setStatus(currentStatus, self.constructActivitiesList(remove=2))

	#def setWatchingStatus(self, show, metadata={}): 

	def removeWatchingStatus(self):
		currentStatus = self.gatewayobj.session.userSettings["status"]
		self.gatewayobj.request.setStatus(currentStatus, self.constructActivitiesList(remove=3))

	def setCustomStatus(self, customstatus):
		currentStatus = self.gatewayobj.session.userSettings["status"]
		self.gatewayobj.request.setStatus(currentStatus, self.constructActivitiesList(updates={4:{"type":4, "state": customstatus, "name":"Custom Status", "emoji": None}}))

	def removeCustomStatus(self):
		currentStatus = self.gatewayobj.session.userSettings["status"]
		self.gatewayobj.request.setStatus(currentStatus, self.constructActivitiesList(remove=4))
#parses response from gateway

class UserParse(object):
	@staticmethod
	def sessions_replace(response, session_id):
		importantdata = {}
		activeCounter = {} #priority = 0
		allCounter = {} #priority = 1
		sessionidCounter = {} #priority = 2
		#sessions_replace is one of those undocumented events that have weird formatting. :(
		for session in response['d']:
			if session.get("active") == True:
				activeCounter = session
				break; #no need to check anything else
			elif session.get("session_id") == "all":
				allCounter = session
			elif session.get("session_id") == session_id:
				sessionidCounter = session
		#now start the processing
		if len(activeCounter) > 0:
			importantdata["status"] = activeCounter["status"]
			importantdata["activities"] = {i["type"]:i for i in activeCounter["activities"]}
			return importantdata
		elif len(allCounter) > 0:
			importantdata["status"] = allCounter["status"]
			importantdata["activities"] = {j["type"]:j for j in allCounter["activities"]}
			return importantdata
		elif len(sessionidCounter) > 0:
			importantdata["status"] = sessionidCounter["status"]
			importantdata["activities"] = {k["type"]:k for k in sessionidCounter["activities"]}
			return importantdata
		else:
			return {}

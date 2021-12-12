import time

def calculateNonce(date="now"):
	if date == "now":
		unixts = time.time()
	else:
		import datetime
		unixts = time.mktime(date.timetuple())
	return str((int(unixts)*1000-1420070400000)*4194304)
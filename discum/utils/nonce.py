import time, datetime

def calculateNonce(date="now"):
	if date == "now":
		date = datetime.datetime.now()
	unixts = time.mktime(date.timetuple())
	return str((int(unixts)*1000-1420070400000)*4194304)
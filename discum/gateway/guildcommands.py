#just a bunch of wrappers
class guildcommands:
	def __init__(self, gatewayobject):
		self.gatewayobject = gatewayobject
		self.currentGuild = ""
		self.channelData = {} #gets cleared every time self.currentGuild changes

	#calculate
	def rangeCalc(self, memberCount):
		ranges = []
		for i in range(int(memberCount/100)+1):
			rangechunk = [[100*j, 100*j+99] for j in range(i+1)]
			if len(rangechunk)>3: 
				del rangechunk[1:-2]
			ranges.append(rangechunk)
		return ranges

	def parseSyncData(self, memberData):
		memberlist = []
		for i in memberData['d']['ops']:
			if 'items' in i:
				for j in i['items']:
					if 'member' in j:
						memberlist.append(j['member'])
		return memberlist

	#send
	def listen(self, guildID, channelID, memberRange, typing=True, activities=True, members=[]):
		self.currentGuild = guildID
		sendData = {"op":14,"d":{"guild_id":self.currentGuild, "channels":{channelID: memberRange}}}
		if typing != None: sendData["d"]["typing"] = typing
		if activities != None: sendData["d"]["activities"] = activities
		if members != None: sendData["d"]["members"] = members
		self.gatewayobject.send(sendData)


	def searchMembers(self, guildIDs, query, limit=10, presences=True): #idk bout the name...what does it do exactly?? what are its limits??
		if isinstance(guildIDs, str):
			guildIDs = [guildIDs]
		self.gatewayobject.send({"op":8,"d":{"guild_id":guildIDs,"query":query,"limit":limit,"presences":presences}})

	def notSureWhatTheseAre(self, guildID):
		self.gatewayobject.send({"op":14,"d":{"guild_id":guildID,"members":[]}}) #completely useless it seems...didnt get any meaningful data back

	#event (receive)
	def GuildMemberListUpdate(self, resp, GUILD_MEMBER_LIST_UPDATE_type=None):
		if resp['t'] == 'GUILD_MEMBER_LIST_UPDATE':
			if GUILD_MEMBER_LIST_UPDATE_type:
				for itemchunk in resp['d']['ops']:
					if GUILD_MEMBER_LIST_UPDATE_type == itemchunk['op']:
						return True
				return False
			return True
		return False

	def GuildCreate(self, resp):
		if resp['t'] == 'GUILD_CREATE':
			return True
		return False

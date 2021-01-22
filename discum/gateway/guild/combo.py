#points to commands that help request info/actions using the gateway
#note, no need for importing GuildParse because resp is a Resp object (resp.parsed... does the trick)
#also, no need for importing GuildRequest because gatewayobj has that (self.gatewayobj.request... does the trick)

import time

class GuildCombo(object):
	def __init__(self, gatewayobj):
		self.gatewayobj = gatewayobj

	def reformat_member(self, memberdata, keep=[]): #memberdata comes in as a dict and leaves as a tuple (userID, memberdatareformatted). This is done to easily prevent duplicates in the member list when fetching.
		allProperties = ['pending', 'deaf', 'hoisted_role', 'presence', 'joined_at', 'public_flags', 'username', 'avatar', 'discriminator', 'premium_since', 'roles', 'is_pending', 'mute', 'nick', 'bot']
		if keep == None:
			remove = allProperties
		elif keep == "all":
			remove = []
		elif isinstance(keep, list):
			remove = list(set(allProperties) - set(keep))
		memberproperties = memberdata['member'] if 'member' in memberdata else memberdata
		userdata = memberproperties.pop('user', {})
		userID = userdata.pop('id', {})
		memberproperties.update(userdata)
		#filtering/removing
		if 'pending' in remove and 'pending' in memberproperties:
			del memberproperties['pending']
		if 'deaf' in remove and 'deaf' in memberproperties:
			del memberproperties['deaf']
		if 'hoisted_role' in remove and 'hoisted_role' in memberproperties:
			del memberproperties['hoisted_role']
		if 'presence' in remove and 'presence' in memberproperties:
			del memberproperties['presence']
		if 'joined_at' in remove and 'joined_at' in memberproperties:
			del memberproperties['joined_at']
		if 'public_flags' in remove and 'public_flags' in memberproperties:
			del memberproperties['public_flags']
		if 'username' in remove and 'username' in memberproperties:
			del memberproperties['username']
		if 'avatar' in remove and 'avatar' in memberproperties:
			del memberproperties['avatar']
		if 'discriminator' in remove and 'discriminator' in memberproperties:
			del memberproperties['discriminator']
		if 'premium_since' in remove and 'premium_since' in memberproperties:
			del memberproperties['premium_since']
		if 'roles' in remove and 'roles' in memberproperties:
			del memberproperties['roles']
		if 'is_pending' in remove and 'is_pending' in memberproperties:
			del memberproperties['is_pending']
		if 'mute' in remove and 'mute' in memberproperties:
			del memberproperties['mute']
		if 'nick' in remove and 'nick' in memberproperties:
			del memberproperties['nick']
		if 'bot' in remove and 'bot' in memberproperties:
			del memberproperties['bot']
		return userID, memberproperties

	def rangeCorrector(self, ranges): #just adds [0,99] at the beginning
		if [0,99] not in ranges:
			ranges.insert(0, [0,99])
		return ranges

	def getIndex(self, guild_id):
		return self.gatewayobj.memberFetchingStatus[guild_id]

	def getRanges(self, index, multiplier):
		initialNum = int(index*multiplier)
		return self.rangeCorrector([[initialNum, initialNum+99], [initialNum+100, initialNum+199]])

	def fetchMembers(self, resp, guild_id, channel_id, method="overlap", keep=[], considerUpdates=True, indexStart=0, reset=True, wait=None): #process is a little simpler than it looks. Keep in mind that there's no actual api endpoint to get members so this is a bit hacky. However, the method used below mimics how the official client loads the member list.
		if self.gatewayobj.READY:
			if self.gatewayobj.memberFetchingStatus.get(guild_id) == None: #request for lazy request
				self.gatewayobj.memberFetchingStatus[guild_id] = indexStart
				if not self.gatewayobj.session.guild(guild_id).hasMembers or reset:
					self.gatewayobj.session.guild(guild_id).resetMembers() #reset
				if len(self.gatewayobj.memberFetchingStatus["first"]) == 0:
					self.gatewayobj.memberFetchingStatus["first"] = [guild_id]
					self.gatewayobj.request.lazyGuild(guild_id, {channel_id: [[0,99]]}, typing=True, threads=False, activities=True, members=[])
				else:
					self.gatewayobj.request.lazyGuild(guild_id, {channel_id: [[0,99]]}, typing=True, activities=True)
			if self.gatewayobj.memberFetchingStatus.get(guild_id) != None and not self.gatewayobj.finishedMemberFetching(guild_id): #proceed with lazy requests
				index = self.getIndex(guild_id)
				#find multiplier (this dictates the way the member list requested for).
				if method == "overlap": multiplier = 100
				elif method == "no overlap": multiplier = 200
				elif isinstance(method, int): multiplier = method
				elif isinstance(method, list) or isinstance(method, tuple): 
					if index<len(method):
						multiplier = method[index]
					else:
						endFetching = True #ends fetching right after resp parsed
				ranges = self.getRanges(index, multiplier)
				#0th lazy request
				if index == indexStart and not self.gatewayobj.session.guild(guild_id).unavailable:
					self.gatewayobj.memberFetchingStatus[guild_id] += 1
					self.gatewayobj.request.lazyGuild(guild_id, {channel_id: ranges})
				elif resp.event.guild_member_list:
					parsed = resp.parsed.guild_member_list_update()
					if parsed['guild_id'] == guild_id and ('SYNC' in parsed['types'] or 'UPDATE' in parsed['types']):
						endFetching = False
						for ind,i in enumerate(parsed['types']):
							if i == 'SYNC':
								if self.gatewayobj.memberFetchingStatus[guild_id]!="done" and (self.gatewayobj.memberFetchingStatus[guild_id] - index) == 0:
									self.gatewayobj.memberFetchingStatus[guild_id] += 1
								if len(parsed['updates'][ind]) == 0 and parsed['locations'][ind] in ranges[1:]: #checks if theres nothing in the SYNC data
									endFetching = True
								for item in parsed['updates'][ind]:
									if 'member' in item:
										member_id, member_properties = self.reformat_member(item, keep=keep)
										self.gatewayobj.session.guild(guild_id).updateOneMember(member_id, member_properties)
										if self.gatewayobj.log: print('<SYNC> updated member '+member_id)
							elif i == 'UPDATE' and considerUpdates: #this really only becomes useful for large guilds (because fetching members can take a quite some time for those guilds)
								for key in parsed['updates'][ind]:
									if key == 'member':
										member_id, member_properties = self.reformat_member(parsed['updates'][ind][key], keep=keep)
										self.gatewayobj.session.guild(guild_id).updateOneMember(member_id, member_properties)
										if self.gatewayobj.log: print('<UPDATE> updated member '+member_id)
							elif i == 'INVALIDATE':
								if parsed['locations'][ind] in ranges or parsed['member_count'] == 0:
									endFetching = True
						if ranges[-2][-1]>self.gatewayobj.session.guild(guild_id).memberCount or ranges[-1][-1]>self.gatewayobj.session.guild(guild_id).memberCount or endFetching: #putting whats most likely to happen first
							self.gatewayobj.memberFetchingStatus[guild_id] = "done"
							self.gatewayobj.removeCommand(
							    {
							        "function": self.fetchMembers,
							        "params": {
							            "guild_id": guild_id,
							            "channel_id": channel_id,
							            "method": method,
							            "keep": keep,
							            "considerUpdates": considerUpdates,
							            "indexStart": indexStart,
							            "reset": reset,
							            "wait": wait,
							        },
							    }
							)
						elif self.gatewayobj.memberFetchingStatus[guild_id]!="done" and (self.gatewayobj.memberFetchingStatus[guild_id] - index) == 1:
							index = self.getIndex(guild_id)
							ranges = self.getRanges(index, multiplier)
							if wait!=None: time.sleep(wait)
							self.gatewayobj.request.lazyGuild(guild_id, {channel_id: ranges})

	#the following 2 are test functions to show how the fetchMembers combo function works, might be removed in a later update
	def testfunc(self, resp):
		self.gatewayobj.removeCommand(self.testfunc)
		print('testfunc')
		pass

	def testfuncPOG(self, resp, pog):
		print('testfuncPOG')
		if pog:
			self.gatewayobj.removeCommand(self.testfuncPOG)
		pass

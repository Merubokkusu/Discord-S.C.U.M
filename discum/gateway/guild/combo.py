#points to commands that help request info/actions using the gateway
#note, no need for importing GuildParse because resp is a Resp object (resp.parsed... does the trick)
#also, no need for importing GuildRequest because gatewayobj has that (self.gatewayobj.request... does the trick)

import time
import copy
import re
from ...utils.permissions import PERMS, Permissions
from ...logger import *

class GuildCombo(object):
	__slots__ = ['gatewayobj']
	def __init__(self, gatewayobj):
		self.gatewayobj = gatewayobj

	#fetchMembers helper function
	def reformat_member(self, memberdata, keep=[]): #memberdata comes in as a dict and leaves as a tuple (userID, memberdatareformatted). This is done to easily prevent duplicates in the member list when fetching.
		allProperties = ['pending', 'deaf', 'hoisted_role', 'presence', 'joined_at', 'public_flags', 'username', 'avatar', 'discriminator', 'premium_since', 'roles', 'is_pending', 'mute', 'nick', 'bot', 'communication_disabled_until']
		if keep == None:
			remove = allProperties
		elif keep == "all":
			remove = []
		elif isinstance(keep, list) or isinstance(keep, tuple):
			remove = list(set(allProperties) - set(keep))
		elif isinstance(keep, str):
			remove = [i for i in allProperties if i!=keep]
		memberproperties = copy.deepcopy(memberdata['member']) if 'member' in memberdata else copy.deepcopy(memberdata)
		userdata = memberproperties.pop('user', {})
		userID = userdata.pop('id', {})
		memberproperties.update(userdata)
		#filtering/removing
		for r in remove:
			if r in memberproperties:
				del memberproperties[r]
		return userID, memberproperties

	#fetchMembers helper function
	def rangeCorrector(self, ranges): #just adds [0,99] at the beginning
		if [0,99] not in ranges:
			ranges.insert(0, [0,99])
		return ranges

	#fetchMembers helper function
	def getIndex(self, guild_id):
		return self.gatewayobj.memberFetchingStatus[guild_id][1]

	#fetchMembers helper function
	def getRanges(self, index, multiplier, memberCount):
		initialNum = int(index*multiplier)
		rangesList = [[initialNum, initialNum+99]]
		if memberCount > initialNum+99:
			rangesList.append([initialNum+100, initialNum+199])
		return self.rangeCorrector(rangesList)

	#fetchMembers helper function
	def updateCurrent(self, guild_id):
		if not self.gatewayobj.finishedMemberFetching(guild_id): #yep still gotta check for this
			self.gatewayobj.memberFetchingStatus[guild_id][1] = self.gatewayobj.memberFetchingStatus[guild_id][0]+1

	#fetchMembers helper function
	def updatePrevious(self, guild_id):
		if not self.gatewayobj.finishedMemberFetching(guild_id):
			self.gatewayobj.memberFetchingStatus[guild_id][0] = self.gatewayobj.memberFetchingStatus[guild_id][1]

	#todo: make channel_id optional (make a helper method to find the "optimal" channel). Also...maybe rewrite fetchMembers to simply code a bit??
	def fetchMembers(self, resp, guild_id, channel_id, method, keep, considerUpdates, startIndex, stopIndex, reset, wait): #process is a little simpler than it looks. Keep in mind that there's no actual api endpoint to get members so this is a bit hacky. However, the method used below mimics how the official client loads the member list.
		if self.gatewayobj.READY:
			if self.gatewayobj.memberFetchingStatus.get(guild_id) == None: #request for lazy request
				self.gatewayobj.memberFetchingStatus[guild_id] = [startIndex, startIndex] #format is [previous index, current index]. This format is useful for the wait parameter.
				if not self.gatewayobj.session.guild(guild_id).hasMembers and reset:
					self.gatewayobj.session.guild(guild_id).resetMembers() #reset
				if len(self.gatewayobj.memberFetchingStatus["first"]) == 0:
					self.gatewayobj.memberFetchingStatus["first"] = [guild_id]
					self.gatewayobj.request.lazyGuild(guild_id, {channel_id: [[0,99]]}, typing=True, threads=False, activities=True, members=[])
				else:
					self.gatewayobj.request.lazyGuild(guild_id, {channel_id: [[0,99]]}, typing=True, activities=True)
			if self.gatewayobj.memberFetchingStatus.get(guild_id) != None and not self.gatewayobj.finishedMemberFetching(guild_id): #proceed with lazy requests
				index = self.getIndex(guild_id) #index always has the current value
				endFetching = False
				#find multiplier (this dictates the way the member list requested for)
				if method == "overlap": multiplier = 100
				elif method == "no overlap": multiplier = 200
				elif isinstance(method, int): multiplier = method
				elif isinstance(method, list) or isinstance(method, tuple): 
					if index<len(method):
						multiplier = method[index]
					else:
						endFetching = True #ends fetching right after resp parsed
				ranges = self.getRanges(index, multiplier, self.gatewayobj.session.guild(guild_id).memberCount) if not endFetching else [[0],[0]]
				#0th lazy request (separated from the rest because this happens "first")
				if index == startIndex and not self.gatewayobj.session.guild(guild_id).unavailable:
					self.updateCurrent(guild_id) #current = previous+1
					if wait!=None: time.sleep(wait)
					self.gatewayobj.request.lazyGuild(guild_id, {channel_id: ranges})
				if resp.event.guild_member_list:
					parsed = resp.parsed.guild_member_list_update()
					if parsed['guild_id'] == guild_id and ('SYNC' in parsed['types'] or 'UPDATE' in parsed['types']):
						endFetching = False
						for ind,i in enumerate(parsed['types']):
							if i == 'SYNC':
								if len(parsed['updates'][ind]) == 0 and parsed['locations'][ind] in ranges[1:]: #checks if theres nothing in the SYNC data
									endFetching = True
									break
								for item in parsed['updates'][ind]:
									if 'member' in item:
										member_id, member_properties = self.reformat_member(item, keep=keep)
										self.gatewayobj.session.guild(guild_id).updateOneMember(member_id, member_properties)
										Logger.log('[gateway] [fetchMembers] <SYNC> updated member '+member_id, None, self.gatewayobj.log)
								if not self.gatewayobj.finishedMemberFetching(guild_id) and (index-self.gatewayobj.memberFetchingStatus[guild_id][0])==1:
									if wait!=None: time.sleep(wait)
									self.updatePrevious(guild_id) #previous = current
							elif i == 'UPDATE' and considerUpdates: #this really only becomes useful for large guilds (because fetching members can take a quite some time for those guilds)
								for key in parsed['updates'][ind]:
									if key == 'member':
										member_id, member_properties = self.reformat_member(parsed['updates'][ind][key], keep=keep)
										self.gatewayobj.session.guild(guild_id).updateOneMember(member_id, member_properties)
										Logger.log('[gateway] [fetchMembers] <UPDATE> updated member '+member_id, None, self.gatewayobj.log)
							elif i == 'INVALIDATE':
								if parsed['locations'][ind] in ranges or parsed['member_count'] == 0:
									endFetching = True
									break
						numFetched = len(self.gatewayobj.session.guild(guild_id).members)
						roundedUpFetched = numFetched-(numFetched%-100) #https://stackoverflow.com/a/14092788/14776493
						if ranges==[[0],[0]] or index>=stopIndex or roundedUpFetched>=self.gatewayobj.session.guild(guild_id).memberCount or endFetching or ranges[1][0]+100>self.gatewayobj.session.guild(guild_id).memberCount: #putting whats most likely to happen first
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
							            "startIndex": startIndex,
							            "stopIndex": stopIndex,
							            "reset": reset,
							            "wait": wait
							        },
							    }
							) #it's alright if you get a "not found in _after_message_hooks" error log. That's not an error for this situation.
						elif not self.gatewayobj.finishedMemberFetching(guild_id) and index==self.gatewayobj.memberFetchingStatus[guild_id][0]:
							self.updateCurrent(guild_id) #current = previous + 1
							self.gatewayobj.request.lazyGuild(guild_id, {channel_id: ranges})


	#helper method for subscribeToGuildEvents
	def findVisibleChannels(self, guildID, types, findFirst):
		channelIDs = []
		if types == "all":
			types = ['guild_text', 'dm', 'guild_voice', 'group_dm', 'guild_category', 'guild_news', 'guild_store', 'guild_news_thread', 'guild_public_thread', 'guild_private_thread', 'guild_stage_voice']
		s = self.gatewayobj.session
		channels = s.guild(guildID).channels
		for channel in channels.values():
			if channel['type'] in types:
				permissions = Permissions.calculatePermissions(s.user['id'], guildID, s.guild(guildID).owner, s.guild(guildID).roles, s.guild(guildID).me['roles'], channel["permission_overwrites"])
				if Permissions.checkPermissions(permissions, PERMS.VIEW_CHANNEL):
					if findFirst:
						return [channel['id']]
					else:
						channelIDs.append(channel['id'])
		return channelIDs

	def subscribeToGuildEvents(self, onlyLarge, wait):
		if self.gatewayobj.READY:
			s = self.gatewayobj.session
			guildIDs = s.guildIDs
			first = {"channel_ranges":{}, "typing":True, "threads":True, "activities":True, "members":[], "thread_member_lists":[]}
			rest = {"channel_ranges":{}, "typing":True, "activities":True, "threads":True}
			for guildID in guildIDs:
				#skip if needed (onlyLarge checking)
				if onlyLarge and not (s.guild(guildID).unavailable or s.guild(guildID).large):
					continue
				#op 14 field construction
				op14fields = {"guild_id":guildID}
				if guildID == guildIDs[0]:
					op14fields.update(first)
					if not s.guild(guildID).unavailable:
						findChannel = self.findVisibleChannels(guildID, types="all", findFirst=True)
						if findChannel:
							op14fields["channel_ranges"] = {findChannel[0]: [[0,99]]}
				else:
					op14fields.update(rest)
					if not s.guild(guildID).unavailable:
						findChannel = self.findVisibleChannels(guildID, types="all", findFirst=True)
						if findChannel:
							op14fields["channel_ranges"] = {findChannel[0]: [[0,99]]}
				#sending the request
				if wait: time.sleep(wait)
				self.gatewayobj.memberFetchingStatus["first"].append(guildID)
				self.gatewayobj.request.lazyGuild(**op14fields)

	#helper for searchGuildMembers
	def handleGuildMemberSearches(self, resp, guildIDs, saveAsQuery, isQueryOverridden, userIDs, keep): #hm what happens if all userIDs are found? well good news: "not_found" value is just []
		if resp.event.guild_members_chunk:
			chunk = resp.parsed.auto()
			gID = chunk["guild_id"]
			match = False
			if gID in guildIDs:
				if userIDs and "not_found" in chunk:
					match = True
					for member in chunk["members"]:
						member_id, member_properties = self.reformat_member(member, keep=keep)
						self.gatewayobj.guildMemberSearches[gID]["ids"].add(member_id)
						self.gatewayobj.session.guild(gID).updateOneMember(member_id, member_properties)
				elif not userIDs:
					if isQueryOverridden:
						match = True #no checks
						for member in chunk["members"]:
							member_id, member_properties = self.reformat_member(member, keep=keep)
							self.gatewayobj.guildMemberSearches[gID]["queries"][saveAsQuery].add(member_id)
							self.gatewayobj.session.guild(gID).updateOneMember(member_id, member_properties)
					else: #check results
						if all([(re.sub(' +', ' ', k["user"]["username"].lower()).startswith(saveAsQuery) or re.sub(' +', ' ', k["nick"].lower()).startswith(saveAsQuery)) if k.get('nick') else re.sub(' +', ' ', k["user"]["username"].lower()).startswith(saveAsQuery) for k in chunk["members"]]): #search user/nick, ignore case, replace consecutive spaces with 1 space
							match = True
							for member in chunk["members"]:
								member_id, member_properties = self.reformat_member(member, keep=keep)
								self.gatewayobj.guildMemberSearches[gID]["queries"][saveAsQuery].add(member_id)
								self.gatewayobj.session.guild(gID).updateOneMember(member_id, member_properties)
				if chunk["chunk_index"] == chunk["chunk_count"]-1 and gID==guildIDs[-1]: #if at end
					if match:
						self.gatewayobj.removeCommand(
							{
								"function": self.handleGuildMemberSearches,
								"params": {
									"guildIDs": guildIDs,
									"saveAsQuery": saveAsQuery,
									"isQueryOverridden": isQueryOverridden,
									"userIDs": userIDs, 
									"keep": keep
								},
							}
						)

	def searchGuildMembers(self, guildIDs, query, saveAsQueryOverride, limit, presences, userIDs, keep):
		if self.gatewayobj.READY:
			saveAsQuery = query.lower() if saveAsQueryOverride==None else saveAsQueryOverride.lower()
			#create a spot to put the data in bot.gateway.guildMemberSearches
			if userIDs: #userID storage
				for i in guildIDs:
					if i not in self.gatewayobj.guildMemberSearches:
						self.gatewayobj.guildMemberSearches[i] = {"ids":set()}
					if "ids" not in self.gatewayobj.guildMemberSearches[i]:
						self.gatewayobj.guildMemberSearches[i]["ids"] = set()
			else: #query storage (saveAsQuery)
				for k in guildIDs:
					if k not in self.gatewayobj.guildMemberSearches:
						self.gatewayobj.guildMemberSearches[k] = {"queries":{}}
					if "queries" not in self.gatewayobj.guildMemberSearches[k]:
						self.gatewayobj.guildMemberSearches[k]["queries"] = {}
					if saveAsQuery not in self.gatewayobj.guildMemberSearches[k]["queries"]:
						self.gatewayobj.guildMemberSearches[k]["queries"][saveAsQuery] = set()
			self.gatewayobj.command(
				{
					"function": self.handleGuildMemberSearches,
					"priority": 0,
					"params": {
						"guildIDs": guildIDs,
						"saveAsQuery": saveAsQuery,
						"isQueryOverridden": saveAsQueryOverride != None,
						"userIDs": userIDs,
						"keep": keep,
					},
				}
			)
			self.gatewayobj.request.searchGuildMembers(guildIDs, query, limit, presences, userIDs)

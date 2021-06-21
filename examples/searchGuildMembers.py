#search guild members aka opcode 8 aka replacement for bot.getGuildMember()

import discum
bot = discum.Client(token='something')

#these functions are still in the test phase, but they'll eventually be moved into discum (after a few changes and bugs get found/removed)
import re #for removing consecutive spaces
from discum.gateway.guild.combo import GuildCombo #for member formatting (reformat_member)

bot.gateway.guildMemberSearches = {}

#move to gateway/guild/combo.py
def handleGuildMemberSearches(resp, guildIDs, saveAsQuery, isQueryOverridden, userIDs): #hm what happens if all userIDs are found? well good news: "not_found" value is just []
	if resp.event.guild_members_chunk:
		chunk = resp.parsed.auto()
		gID = chunk["guild_id"]
		match = False
		if gID in guildIDs:
			if userIDs and "not_found" in chunk:
				match = True
				for member in chunk["members"]:
					member_id, member_properties = GuildCombo(bot.gateway).reformat_member(member, keep="all")
					bot.gateway.guildMemberSearches[gID]["ids"].add(member_id)
					bot.gateway.session.guild(gID).updateOneMember(member_id, member_properties)
			elif not userIDs:
				if isQueryOverridden:
					match = True #no checks
					for member in chunk["members"]:
						member_id, member_properties = GuildCombo(bot.gateway).reformat_member(member, keep="all")
						bot.gateway.guildMemberSearches[gID]["queries"][saveAsQuery].add(member_id)
						bot.gateway.session.guild(gID).updateOneMember(member_id, member_properties)
				else: #check results
					if all([(re.sub(' +', ' ', k["user"]["username"].lower()).startswith(saveAsQuery) or re.sub(' +', ' ', k["nick"].lower()).startswith(saveAsQuery)) if k.get('nick') else re.sub(' +', ' ', k["user"]["username"].lower()).startswith(saveAsQuery) for k in chunk["members"]]):
						match = True
						for member in chunk["members"]:
							member_id, member_properties = GuildCombo(bot.gateway).reformat_member(member, keep="all")
							bot.gateway.guildMemberSearches[gID]["queries"][saveAsQuery].add(member_id)
							bot.gateway.session.guild(gID).updateOneMember(member_id, member_properties)
			if chunk["chunk_index"] == chunk["chunk_count"]-1 and gID==guildIDs[-1]: #if at end
				if match:
					bot.gateway.removeCommand(
						{
							"function": handleGuildMemberSearches,
							"params": {
								"guildIDs": guildIDs,
								"saveAsQuery": saveAsQuery,
								"isQueryOverridden": isQueryOverridden,
								"userIDs": userIDs
							},
						}
					)

#move to gateway/guild/combo.py
def searchGuildMembers(guildIDs, query="", saveAsQueryOverride=None, limit=10, presences=True, userIDs=None):
	if bot.gateway.READY:
		saveAsQuery = query.lower() if saveAsQueryOverride==None else saveAsQueryOverride.lower()
		#create a spot to put the data in bot.gateway.guildMemberSearches
		if userIDs: #userID storage
			for i in guildIDs:
				if i not in bot.gateway.guildMemberSearches:
					bot.gateway.guildMemberSearches[i] = {"ids":set()}
				if "ids" not in bot.gateway.guildMemberSearches[i]:
					bot.gateway.guildMemberSearches[i]["ids"] = set()
		else: #query storage (saveAsQuery)
			for k in guildIDs:
				if k not in bot.gateway.guildMemberSearches:
					bot.gateway.guildMemberSearches[k] = {"queries":{}}
				if "queries" not in bot.gateway.guildMemberSearches[k]:
					bot.gateway.guildMemberSearches[k]["queries"] = {}
				if saveAsQuery not in bot.gateway.guildMemberSearches[k]["queries"]:
					bot.gateway.guildMemberSearches[k]["queries"][saveAsQuery] = set()
		bot.gateway.command({"function":handleGuildMemberSearches, "priority":0, "params": {"guildIDs":guildIDs, "saveAsQuery":saveAsQuery, "isQueryOverridden":saveAsQueryOverride!=None, "userIDs":userIDs}})
		bot.gateway.request.searchGuildMembers(guildIDs, query, limit, presences, userIDs) #not in combo.py bc we only want this to send once

#move to gateway/gateway.py
def finishedGuildSearch(guildIDs, query="", saveAsQueryOverride=None, userIDs=None):
	saveAsQuery = query.lower() if saveAsQueryOverride==None else saveAsQueryOverride.lower()
	return {"function": handleGuildMemberSearches, "params": {"guildIDs": guildIDs, "saveAsQuery": saveAsQuery, "isQueryOverridden": saveAsQueryOverride!=None, "userIDs": userIDs}} not in bot.gateway._after_message_hooks

######################################################################
#how to run:

#EXAMPLE 1: query member search in guild(s)
@bot.gateway.command
def test(resp):
	if resp.event.ready_supplemental:
		searchGuildMembers(['guildID'], 'searchTerm', limit=100)
	if resp.event.guild_members_chunk and finishedGuildSearch(['guildID'], 'searchTerm'):
		bot.gateway.close()

bot.gateway.run()

print(bot.gateway.guildMemberSearches)
bot.gateway.clearCommands()

#EXAMPLE 2: search for userID(s) in guild(s)
@bot.gateway.command
def test(resp):
	if resp.event.ready_supplemental:
		searchGuildMembers(['guildID'], userIDs=['userID'])
	if resp.event.guild_members_chunk and finishedGuildSearch(['guildID'], userIDs=['userID']):
		bot.gateway.close()

bot.gateway.run()

print(bot.gateway.guildMemberSearches)
bot.gateway.clearCommands()

#EXAMPLE 3: opcode 8 brute forcer
#not entirely random. Optimized quite a bit.

import time

allchars = [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~']
bot.qList = ["!"] #query list
bot.gateway.guildMemberSearches = {}
bot.gateway.resetMembersOnSessionReconnect = False #member list brute forcing can take a while

def calculateOption(guildID, action): #action == 'append' or 'replace'
	if action == 'append':
		lastUserIDs = bot.gateway.guildMemberSearches[guildID]["queries"][''.join(bot.qList)]
		data = [bot.gateway.session.guild(guildID).members[i] for i in bot.gateway.session.guild(guildID).members if i in lastUserIDs]
		lastName = sorted(set([re.sub(' +', ' ', j['nick'].lower()) if (j.get('nick') and re.sub(' +', ' ', j.get('nick').lower()).startswith(''.join(bot.qList))) else re.sub(' +', ' ', j['username'].lower()) for j in data]))[-1]
		try:
			option = lastName[len(bot.qList)]
			return option
		except IndexError:
			return None
	elif action == 'replace':
		if bot.qList[-1] in allchars:
			options = allchars[allchars.index(bot.qList[-1])+1:]
			if ' ' in options and (len(bot.qList)==1 or (len(bot.qList)>1 and bot.qList[-2]==' ')): #cannot start with a space and cannot have duplicate spaces
				options.remove(' ')
			return options
		else:
			return None

def findReplaceableIndex(guildID):
	for i in range(len(bot.qList)-2, -1, -1): #assume that the last index is not changable
		if bot.qList[i] != '~':
			return i
	return None

def bruteForceTest(resp, guildID, wait):
	if resp.event.ready_supplemental:
		searchGuildMembers([guildID], query=''.join(bot.qList), limit=100)
	elif resp.event.guild_members_chunk:
		remove = False
		if len(bot.gateway.guildMemberSearches[guildID]["queries"][''.join(bot.qList)]) == 100: #append
			appendOption = calculateOption(guildID, 'append')
			if appendOption:
				bot.qList.append(appendOption)
			else:
				remove = True
		else: #if <100 results returned, replace
			replaceOptions = calculateOption(guildID, 'replace')
			if replaceOptions:
				bot.qList[-1] = replaceOptions[0]
			else:
				remove = True
		if remove: #if no replace options, find first replaceable index & replace it
			if len(bot.qList) == 1: #reached end of possibilities
				bot.gateway.removeCommand({"function": bruteForceTest, "params":{"guildID":guildID, "wait":wait}})
				bot.gateway.close()
			else:
				replaceableInd = findReplaceableIndex(guildID)
				if replaceableInd != None:
					bot.qList = bot.qList[:replaceableInd+1]
					replaceOptions = calculateOption(guildID, 'replace')
					bot.qList[-1] = replaceOptions[0]
				else:
					bot.gateway.removeCommand({"function": bruteForceTest, "params":{"guildID":guildID, "wait":wait}})
					bot.gateway.close()
		if wait: time.sleep(wait)
		print('next query: '+''.join(bot.qList))
		print('members fetched so far: '+repr(len(bot.gateway.session.guild(guildID).members)))
		print("effectiveness: "+repr(len(bot.gateway.session.guild(guildID).members)/(len(bot.gateway.guildMemberSearches[guildID]["queries"])))+"%")
		searchGuildMembers([guildID], query=''.join(bot.qList), limit=100)

guildID = ''
wait = 1
bot.gateway.command({"function": bruteForceTest, "params":{"guildID":guildID, "wait":wait}})
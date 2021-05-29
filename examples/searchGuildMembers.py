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
		match = False
		if userIDs and "not_found" in chunk:
			for i in guildIDs:
				for member in chunk["members"]:
					member_id, member_properties = GuildCombo(bot.gateway).reformat_member(member, keep="all")
					bot.gateway.guildMemberSearches[i]["ids"].add(member_id)
					bot.gateway.session.guild(i).updateOneMember(member_id, member_properties)
		elif not userIDs:
			for j in guildIDs:
				if isQueryOverridden: #no checks
					match = True
					for member in chunk["members"]:
						member_id, member_properties = GuildCombo(bot.gateway).reformat_member(member, keep="all")
						bot.gateway.guildMemberSearches[j]["queries"][saveAsQuery].add(member_id)
						bot.gateway.session.guild(j).updateOneMember(member_id, member_properties)
				else: #check results
					if all([(re.sub(' +', ' ', k["user"]["username"].lower()).startswith(saveAsQuery) or re.sub(' +', ' ', k["nick"].lower()).startswith(saveAsQuery)) if k.get('nick') else re.sub(' +', ' ', k["user"]["username"].lower()).startswith(saveAsQuery) for k in chunk["members"]]):
						match = True
						for member in chunk["members"]:
							member_id, member_properties = GuildCombo(bot.gateway).reformat_member(member, keep="all")
							bot.gateway.guildMemberSearches[j]["queries"][saveAsQuery].add(member_id)
							bot.gateway.session.guild(j).updateOneMember(member_id, member_properties)
		if chunk["chunk_index"] == chunk["chunk_count"]-1: #if at end
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

#query member search in guild(s)
@bot.gateway.command
def test(resp):
	if resp.event.ready_supplemental:
		searchGuildMembers(['guildID'], 'searchTerm', limit=100)
	if resp.event.guild_members_chunk and finishedGuildSearch(['guildID'], 'searchTerm'):
		bot.gateway.close()

bot.gateway.run()

print(bot.gateway.guildMemberSearches)

bot.gateway.clearCommands()

#search for userID(s) in guild(s)
@bot.gateway.command
def test(resp):
	if resp.event.ready_supplemental:
		searchGuildMembers(['guildID'], userIDs=['userID'])
	if resp.event.guild_members_chunk and finishedGuildSearch(['guildID'], userIDs=['userID']):
		bot.gateway.close()

bot.gateway.run()

print(bot.gateway.guildMemberSearches)

bot.gateway.clearCommands()
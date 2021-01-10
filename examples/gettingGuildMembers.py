# Keep in mind that there's no actual api endpoint for users to get guild members.
# So, to get guild members, we have to request for and read the member list.
# This is all handled with the bot.gateway.fetchMembers(...) function :) . This function can either be run while the gateway is connected or before the gateway connects.
# Note, you'll need to connect to the gateway to get the member list.
# An example usage is below. The Guild and Channel ids used are from the fortnite server (652k members, around 150k of those are actually fetchable).
# The number of fetchable members changes from time to time.
# https://github.com/Merubokkusu/Discord-S.C.U.M/blob/master/docs/using.md#fetch-guild-members

import discum
bot = discum.Client(token='ur token')

@bot.gateway.command
def memberTest(resp):
	guild_id = '322850917248663552'
	channel_id = '754536220826009670'
	if resp.event.ready_supplemental:
		bot.gateway.fetchMembers(guild_id, channel_id)
	if bot.gateway.finishedMemberFetching(guild_id):
		lenmembersfetched = len(bot.gateway.session.guild(guild_id).members)
		print(str(lenmembersfetched)+' members fetched')
		bot.gateway.removeCommand(memberTest)
		bot.gateway.close()

bot.gateway.run()

for memberID in bot.gateway.session.guild('322850917248663552').members:
	print(memberID)

'''
Another possible way to fetchMembers is this (fetchMembers function outside of function memberTest):

import discum
bot = discum.Client(token='ur token')

guild_id = '322850917248663552'
channel_id = '754536220826009670'
bot.gateway.fetchMembers(guild_id, channel_id)

@bot.gateway.command
def memberTest(resp):
	if bot.gateway.finishedMemberFetching('322850917248663552'):
		lenmembersfetched = len(bot.gateway.session.guild('322850917248663552').members)
		print(str(lenmembersfetched)+' members fetched')
		bot.gateway.removeCommand(memberTest)
		bot.gateway.close()

bot.gateway.run()

for memberID in bot.gateway.session.guild('322850917248663552').members:
	print(memberID)

'''

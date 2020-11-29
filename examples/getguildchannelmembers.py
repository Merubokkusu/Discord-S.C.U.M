'''
working get-guild-members function
This will get all the guild members that your client can see (from the members sidebar).
This will eventually (maybe a few days, idk) be put into discum, made prettier (cause this code looks horrendous rn ngl), and get optimized, but I just wanted to upload this now cause I'm happy it works lol.
'''

#notice how all these variables are bot.something
#That's done so that the decorated getGuildChannelMembers function can access them while running. When I add a getGuildChannelMembers or getGuildMembers function it'll look a lot prettier ofc.

import discum
bot = discum.Client(token=token)

bot.memberlist = []
bot.memberRanges = False
bot.index = 0

#set guild and channel variables
bot.guildID = "713308757529985086"
bot.channelID = "713309316052156536" #you need to specify a channel ID

@bot.gateway.command
def getGuildChannelMembers(resp):
	if resp['t'] == 'READY_SUPPLEMENTAL': #tells the program when to start requesting for guild members
		bot.memberRanges = bot.gateway.guildcommands.rangeCalc(bot.gateway.session.guild(bot.guildID).memberCount)
	if bot.memberRanges != False:
		if bot.index == 0:
			bot.gateway.guildcommands.listen(bot.guildID,bot.channelID, memberRange=bot.memberRanges[bot.index])
			bot.index += 1
		if bot.gateway.guildcommands.GuildMemberListUpdate(resp,'SYNC'):
			bot.memberlist.extend(bot.gateway.guildcommands.parseSyncData(resp))
			if bot.index == len(bot.memberRanges): #because we want to end it on the last SYNC
				bot.gateway.close()
			if bot.index != len(bot.memberRanges):
				bot.gateway.guildcommands.listen(bot.guildID,bot.channelID, memberRange=bot.memberRanges[bot.index], typing=None, activities=None)
				bot.index += 1

bot.gateway.run()

memberlist = list({i['user']['id']:i for i in bot.memberlist}.values()) #remove duplicates, just in case

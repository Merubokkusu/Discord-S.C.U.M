'''
Below are examples on how to search and trigger slash commands (like /saved queues create test).
'''

#The following example is the recommended way for triggering slash commands in a guild.
from discum.utils.slash import SlashCommander

def slashCommandTest(resp, guildID, channelID, botID):
	if resp.event.ready_supplemental:
		bot.gateway.request.searchSlashCommands(guildID, limit=10, query="saved") #query slash cmds
	if resp.event.guild_application_commands_updated:
		bot.gateway.removeCommand(slashCommandTest) #because 2 guild_app_cmd_update events are received...idk ask discord why
		slashCmds = resp.parsed.auto()['application_commands'] #get the slash cmds
		s = SlashCommander(slashCmds, application_id=botID) #for easy slash cmd data creation
		data = s.get(['saved', 'queues', 'create'], inputs={'name':'test'})
		bot.triggerSlashCommand(botID, channelID=channelID, guildID=guildID, data=data, sessionID=bot.gateway.session_id) #and send it off
		bot.gateway.close() #optional. It's better to remove this line actually.

guildID = ""
channelID = ""
botID = "234395307759108106"
bot.gateway.command(
	{
		"function": slashCommandTest,
		"params": {"guildID": guildID, "channelID": channelID, "botID": botID},
	}
)
bot.gateway.run()


#The following example is the recommended for triggering slash commands in a DM

channelID = ""
botID = "234395307759108106"

#first, lets see what slash commands we can run
slashCmds = bot.getSlashCommands(botID).json()

#next, let's parse that and create some slash command data
from discum.utils.slash import SlashCommander
s = SlashCommander(slashCmds) #slashCmds can be either a list of cmds or just 1 cmd. Each cmd is of type dict.
data = s.get(['saved', 'queues', 'create'], inputs={'name':'test'})

#finally, lets send the slash command
bot.triggerSlashCommand(botID, channelID, data=data) #by default, a random session id is generated

'''
It technically doesn't matter which one you use. But, if you'd like to mimic the client,
use the top one in guilds and the bottom one in DMs. 

Also, the searching part is not required. If you have the correct data dictionary, you can just input that
into the bot.triggerSlashCommand function.

Finally, SlashCommander has a total of 3 functions to help you create slash commands:
'''
s = SlashCommander(slashCmds) #first, you need to initialize it

#get type, description, and options of command (from command list)
s.metadata(['saved', 'queues', 'create'])

#get options (attributes and parameters) of command (from command list)
s.options(['saved'])
s.options(['saved', 'queues', 'create'])

#get constructed slash command data
s.get(['saved', 'queues', 'create'], inputs={'name':'test'})

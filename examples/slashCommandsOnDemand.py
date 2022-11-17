'''
Below is an example on how to search and trigger slash commands of other bots (like /imagine) on demand from any user on the channel, based on a keyword.
The below example will allow any user in the specified channel to write: '--mycommand hello there' which will trigger another bots slash command: '/imagine hello there'
You can build on it and add other keywords with other associated actions.
'''


from discum.utils.slash import SlashCommander
import discum

# DEFINE CONTSTANTS/VARIABLES

bot = discum.Client(token='AAAAAAAAAAABBBBBBBBBBBBBBCCCCCCCCCCCCCCCCCCC')
guildID = "1111111111111111"
channelID = "2222222222222222"
botID = "33333333333333333"
keyword_1 = '--mycommand '

# DEFINE METHODS

def slashCommandTest(resp, guildID):
    if resp.event.ready_supplemental:
        bot.gateway.request.searchSlashCommands(guildID, limit=10, query="imagine")  # query slash cmd, we are only looking for 'imagine' command here
    if resp.event.guild_application_commands_updated:
        bot.gateway.removeCommand(slashCommandTest)             # because 2 guild_app_cmd_update events are received...idk ask discord why
        slashCmds = resp.parsed.auto()['application_commands']  # get the slash cmds
        bot.gateway.command(                                    # register a new gateway command here using the slashCmds that we now have, and trigger the slash command from there. I tried doing it differently for 2 nights, only this way seems to work
            {
                "function": on_message,
                "params": {"slashCmds": slashCmds},
            }
        )


def on_message(resp, slashCmds):

    if resp.event.message:
        message = resp.parsed.auto()
        if message['channel_id'] == channelID:                      	# only allowing this to trigger if the message was sent in specific channel
            if message['content'].startswith(keyword_1):            	# if message starts with the keyword we defined above:

                print('Message starts with the keyword, building slash command...')

                prompt = message['content'].replace(keyword_1, '')  	# remove the keyword
                s = SlashCommander(slashCmds, application_id=botID) 	# for easy slash cmd data creation
                data = s.get(["imagine"], inputs={'prompt': prompt})	# call 'imagine' slash command with the 'prompt' body

                print('Triggering slash command')

                bot.triggerSlashCommand(botID, channelID=channelID, guildID=guildID, data=data, sessionID=bot.gateway.session_id)  # and send it off


# BODY

bot.gateway.command(
    {
        "function": slashCommandTest,
        "params": {"guildID": guildID},
    }
)

bot.gateway.run()



#I don't currently have an example for triggering slash commands on demand in a DM

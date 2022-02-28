#Buttons are weird. Don't just copy paste the 2nd example; explore what the bot sends in response to the interaction (message_create, message_update, etc)

import discum
bot = discum.Client(token='ur token')

'''
1st example: get message and then click on button
'''
#this is a bit easier but has a small chance getting your acc flagged (because, 1 more request need per button click than usual)
from discum.utils.button import Buttoner

guildID = None #replace with guildID string if msg is in a guild
channelID = ""
messageID = ""

#click button
message = bot.getMessage(channelID, messageID)
data = message.json()[0]
buts = Buttoner(data["components"])
bot.click(
    data["author"]["id"],
    channelID=data["channel_id"],
    guildID=guildID,
    messageID=data["id"],
    messageFlags=data["flags"],
    data=buts.getButton("First"),
)

#select dropdown option
message = bot.getMessage(channelID, messageID)
data = message.json()[0]
bot.click(
    data["author"]["id"],
    channelID=data["channel_id"],
    guildID=guildID,
    messageID=data["id"],
    messageFlags=data["flags"],
    data=buts.getMenuSelection(placeholder="Make a selection", labels=['a', 'b']),
)

#note that custom_ids can change after you make an interaction (click on a button, react, etc), 
#so don't forget to fetch the message again before clicking on a button

'''
2nd example: triggering groovy's queue slash cmd and then click on the "First" button
'''
#you don't need to use slash commands ofc. This is just an example that uses Groovy's queue command (which creates a msg w/buttons).
#In general, using the gateway to see new messages & message updates is safer than using get messages REST requests.

from discum.utils.slash import SlashCommander
from discum.utils.button import Buttoner

def slashCommandTest(resp, guildID, channelID, botID):
    if resp.event.ready_supplemental:
        bot.gateway.request.searchSlashCommands(guildID, limit=10, query="queue") #query slash cmds
    if resp.event.guild_application_commands_updated:
        bot.gateway.removeCommand(slashCommandTest) #because 2 guild_app_cmd_update events are received...idk ask discord why
        slashCmds = resp.parsed.auto()['application_commands'] #get the slash cmds
        s = SlashCommander(slashCmds, application_id=botID) #for easy slash cmd data creation
        data = s.get(['queue'])
        bot.triggerSlashCommand(botID, channelID=channelID, guildID=guildID, data=data, sessionID=bot.gateway.session_id) #and send it off
        bot.gateway.command(clickButton)

def clickButton(resp):
    if resp.event.message or resp.event.message_updated:
        data = resp.parsed.auto()
        if data.get("webhook_id") == "234395307759108106" and data["interaction"]["user"]["id"]==bot.gateway.session.user["id"]:
            bot.gateway.close()
            buts = Buttoner(data["components"])
            bot.click(
                data["webhook_id"],
                channelID=data["channel_id"],
                guildID=data.get("guild_id"),
                messageID=data["id"],
                messageFlags=data["flags"],
                data=buts.getButton("First"),
                sessionID=bot.gateway.session_id
            )

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

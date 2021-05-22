#not receiving messages from large guilds? simply run bot.gateway.subscribeToGuildEvents(wait=1) while
#the gateway is running and then you'll get messages from those large guilds

import discum
bot = discum.Client(token='ur token', log=False)

@bot.gateway.command
def helloworld(resp):
    if resp.event.ready_supplemental:
        bot.gateway.subscribeToGuildEvents(wait=1)
    if resp.event.message:
        m = resp.parsed.auto()
        guildID = m['guild_id'] if 'guild_id' in m else None #because DMs are technically channels too
        channelID = m['channel_id']
        username = m['author']['username']
        discriminator = m['author']['discriminator']
        content = m['content']
        print("> guild {} channel {} | {}#{}: {}".format(guildID, channelID, username, discriminator, content))

bot.gateway.run()

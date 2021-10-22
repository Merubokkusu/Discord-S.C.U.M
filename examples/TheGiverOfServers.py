'''
if someone replies to your message in a dm, this code will use a recent bug to give that person the SERVER badge (credits go to https://github.com/divinityseraph/server-badge-exploit)
here's how it looks: https://www.reddit.com/r/discordapp/comments/jzlnlb/discords_new_reply_feature_is_fun_and_bugged_lol/
this bug works both on servers and DMs :). The below code is only for DMs but can be easily modified to work only on guilds or on both.
**idk if this bug still works
'''

import discum
import time

bot = discum.Client(token='ur token')
bot.discord = 'https://discord.com/api/' #modify base url

@bot.gateway.command
def helloworld(resp):
    if resp.event.ready_supplemental: #ready_supplemental is sent after ready
        user = bot.gateway.session.user
        print("Logged in as {}#{}".format(user['username'], user['discriminator']))
    if resp.event.message:
        m = resp.parsed.auto()
        if m['content'] == 'turn me into a server':
            bot.sendMessage(m['channel_id'], 'reply to one of my messages and I will make you a server :)')
        if m['author']['id'] == bot.gateway.session.user['id']:
            return
        if m['type'] == 'reply':
            if 'referenced_message' in m and m['referenced_message']['author']['id'] == bot.gateway.session.user['id']:
                time.sleep(1)
                bot.reply(m['channel_id'], m['id'], "The server Gods have allowed me to grant you the server badge. You are now a server :).")

bot.gateway.run()

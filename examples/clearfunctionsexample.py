import discum
bot = discum.Client(token='ur token')

@bot.gateway.command
def helloworld1(resp):
    if resp.event.ready_supplemental: #ready_supplemental is sent after ready
        user = bot.gateway.session.user
        print("Logged in as {}#{}".format(user['username'], user['discriminator']))

@bot.gateway.command
def helloworld2(resp):
    if resp.event.message:
        print('Detected a message')
        bot.gateway.clearCommands()

bot.gateway.run(auto_reconnect=True)

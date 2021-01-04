import discum
bot = discum.Client(token='ur token')

@bot.gateway.command
def closeexample(resp):
    if resp.event.message:
        print('Detected a message')
        bot.gateway.close()

bot.gateway.run(auto_reconnect=True)

bot.gateway.clearCommands() #run this if you want to clear commands
bot.gateway.resetSession() #run this if you want to clear collected session data from last connection
bot.gateway.run(auto_reconnect=True) #and now you can connect to the gateway server again

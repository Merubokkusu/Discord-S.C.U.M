import discum
bot = discum.Client(token='ur token')

@bot.gateway.command
def sendexample(resp):
    if resp.event.message:
        print('Detected a message')
        bot.gateway.removeCommand(sendexample) #use this if you only want to send the data once
        bot.gateway.send({"op":3,"d":{"status":"dnd","since":0,"activities":[],"afk":False}})

bot.gateway.run(auto_reconnect=True)

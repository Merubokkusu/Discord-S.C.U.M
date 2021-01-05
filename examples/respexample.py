#the following example uses all 3 attributes of resp

import discum
bot = discum.Client(token='ur token')

@bot.gateway.command
def resptest(resp):
	if resp.event.message:
		print(resp.raw) #raw response
		print(resp.parsed.message_create()['type'] == resp.parsed.auto()['type']) #will print True

bot.gateway.run()

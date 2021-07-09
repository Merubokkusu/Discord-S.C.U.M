#login using remote authentication (install discum[ra] first)
import discum
bot = discum.Client(remoteAuth=True)

#or login normally and run this:
bot.initRA()

#now you can use the remote authentication functions, for example:

#this sends the qr code image in a message
#note that qr codes expire after 5 mintues
@bot.ra.command
def test(response):
	if response["op"]=="pending_remote_init":
		bot.sendFile("channel id here", bot.ra.fingerprint+'.png')

bot.ra.run() #if no filename is specified, {fingerprint}.png is assumed
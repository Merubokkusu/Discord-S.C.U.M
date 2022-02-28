Get Started
===========

Installing
----------

Latest version from github:

    python -m pip install --user --upgrade git+https://github.com/Merubokkusu/Discord-S.C.U.M.git#egg=discum

or with remote authentication functions:

    python -m pip install --user --upgrade -e git+https://github.com/Merubokkusu/Discord-S.C.U.M.git#egg=discum[ra]

Previous versions (not recommended):
1) pick a [release](https://github.com/Merubokkusu/Discord-S.C.U.M/releases) and download it
2) in cmd/terminal, cd into the release folder
3) run `python setup.py install`

Initializing your client
------------------------

``` python
import discum
bot = discum.Client(token="user token here")
```

### Parameters:

-   **email** (Optional[str])
-   **password** (Optional[str])
-   **secret** (Optional[str]) - the 2FA secret string
-   **code** (Optional[str]) - TOTP 6 digit code
-   **token** (Optional[str]) - if you'd like to use discum without auth, input an invalid token like "poop"
-   **remote\_auth** (Optional[bool/str]) - use remote authentication (scan qr code) to login. Set as filename if you'd like to set a specific file location for the qr code image. Defaults to True
-   **proxy** (Optional[str])
	examples:       
		"http://10.10.1.10:3128"       
		"http://username:password123@10.10.1.10:3128"       
		"https://10.10.1.10:3126"       
		"socks4://10.10.1.10:3126"       
-   **user\_agent** (Optional[str/list]) - defaults to "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36". Input a list of user agent strings to randomly pick a user agent
-   **locale** (Optional[str]) - defaults to "en-US"
-   **build\_num** (Optional[int]) - defaults to "request", which then requests the discord build number
-   **log** (Optional[dict]) - defaults to {"console":True, "file":False, "encoding":"utf-8"}. The value of "file" can be set to a filename (which is created if it does not exist). The encoding can be specified manually, but setting it to anything other than utf-8 may cause UnicodeEncodeErrors.

### Returns:

a discum.Client object

Examples
--------

A simple example showing how to use the REST api wraps and how to interact with discord's gateway:

``` python
import discum
bot = discum.Client(token='user token here')

bot.sendMessage("238323948859439", "Hello :)")

@bot.gateway.command
def helloworld(resp):
    if resp.event.ready_supplemental: #ready_supplemental is sent after ready
        user = bot.gateway.session.user
        print("Logged in as {}#{}".format(user['username'], user['discriminator']))
    if resp.event.message:
        m = resp.parsed.auto()
        guildID = m['guild_id'] if 'guild_id' in m else None #because DMs are technically channels too
        channelID = m['channel_id']
        username = m['author']['username']
        discriminator = m['author']['discriminator']
        content = m['content']
        print("> guild {} channel {} | {}#{}: {}".format(guildID, channelID, username, discriminator, content))

bot.gateway.run(auto_reconnect=True)
```

An example for logging online friends:

``` python
import discum
bot = discum.Client(token = 'user token here')

bot.usersOnline = []

@bot.gateway.command
def logOnlineUsers(resp):
    if resp.event.ready_supplemental:
        bot.usersOnline = list(bot.gateway.session.onlineFriendIDs)
    if resp.event.presence_updated:
        data = resp.raw['d']
        if "guild_id" not in data and data['status']=='online':
            bot.usersOnline.append(data['user']['id'])

bot.gateway.run()
```

[more examples](https://github.com/Merubokkusu/Discord-S.C.U.M/tree/master/examples)

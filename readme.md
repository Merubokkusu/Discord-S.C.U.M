# DisCum
![version](https://img.shields.io/badge/github%20version-1.4.0-blue) [![python versions](https://img.shields.io/badge/python-2.7%20%7C%203.5%20%7C%203.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-blue)](https://github.com/Merubokkusu/Discord-S.C.U.M)       
[![PyPI version](https://badge.fury.io/py/discum.svg)](https://badge.fury.io/py/discum) [![python versions](https://img.shields.io/badge/python-2.7%20%7C%203.5%20%7C%203.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-green)](https://pypi.org/project/discum)      
A simple, easy to use, non-restrictive, synchronous Discord API Wrapper for Selfbots/Userbots written in Python.       
-using requests and websockets :)

![https://files.catbox.moe/3ns003.png](https://files.catbox.moe/3ns003.png)
        
Will have less and less time to work on this project.          
If you have issues, you can either make an issue, email discordtehe@gmail.com, or ask on https://reddit.com/r/Discord_selfbots.       
For another python library that's currently better maintained, I'd recommend the following (asynchronous) lib: https://github.com/dolfies/discord.py-self           
Happy new year & happy coding,         
\- arandomnewaccount                  
##### *** risky actions: [issue #66](https://github.com/Merubokkusu/Discord-S.C.U.M/issues/66#issue-876713938)

## Table of Contents
- [Key Features](#Key-features)
- [About](#About)
- [Installation](#Installation)
  - [Prerequisites](#prerequisites-installed-automatically-using-above-methods)
- [Documentation](#Documentation)
- [Contributing](#Contributing)
- [Example Usage](#Example-usage)
- [Links](#Links)
- [Checklist](#Checklist)
- [Contributing](#Contributing)
- [FAQ](#FAQ)
- [Notes](#Notes)

## Key features
- easy-to-use (make selfbots/userbots)
- easy-to-extend/edit (add api wrappers)
- readable (organized 😃 )
- mimics the client while giving you control
- all api wraps point to user/"private" apis
- on-event (gateway) capabilities
- [extremely customizable fetchMembers function](docs/using/fetchingGuildMembers.md)
- remote authentication functions
- support for python 2.7

## About
  Discum is a Discord self/userbot api wrapper (in case you didn't know, self/userbotting = automating a user account). Whenever you login to discord, your client communicates with Discord's servers using Discord's http api (http(s) requests) and gateway server (websockets). Discum allows you have this communication with Discord using python. 
  
  The main difference between Discum and other Discord api wrapper libraries (like discord.py) is that discum is written and maintained to work on user accounts (so, perfect for selfbots/userbots). We test code on here and develop discum to be readable, expandable, and useable. Functions that are risky to use are clearly stated as such in the docs.    
  
  Note, using a selfbot is against Discord's Terms of Service and you could get banned for using one if you're not careful. Also, this needs to be said: discum does not have rate limit handling. The main reasons for this are that discum is made to (1) be (relatively) simple and (2) give the developer/user freedom with how to handle the rate limits. We (Merubokkusu and anewrandomaccount) do not take any responsibility for any consequences you might face while using discum. We also do not take any responsibility for any damage caused (to servers/channels) through the use of Discum. Discum is a tool; how you use this tool is on you.

## Installation  
To install the library normally, run:
```
python -m pip install --user --upgrade git+https://github.com/Merubokkusu/Discord-S.C.U.M.git#egg=discum
```
Otherwise, to also use remote authentication functions (login using a phone & qr code), run:
```
python -m pip install --user --upgrade -e git+https://github.com/Merubokkusu/Discord-S.C.U.M.git#egg=discum[ra]
```

#### Prerequisites (installed automatically using above methods)
- requests
- requests_toolbelt
- brotli
- websocket_client==0.59.0
- filetype
- ua-parser
- colorama

remote auth prerequisites (if you install discum[ra]):       
- pyqrcode
- pycryptodome
- pypng

## Documentation
[https://github.com/Merubokkusu/Discord-S.C.U.M/tree/master/docs](docs)

## Contributing
Contributions are welcome. You can submit issues, make pull requests, or suggest features. Ofc not all suggestions will be implemented (because discum is intended to be a transparent, relatively-raw discord user api wrapper), but all suggestions will be looked into.        
Please see the [contribution guidelines](https://github.com/Merubokkusu/Discord-S.C.U.M/blob/master/contributing.md)

# Example usage
```python
import discum     
bot = discum.Client(token='420tokentokentokentoken.token.tokentokentokentokentoken', log=False)

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

# Links
[Documentation](docs)      
[More examples](examples)      
[Changelog](changelog.md)      
[GitHub](https://github.com/Merubokkusu/Discord-S.C.U.M)      
[PyPi](https://pypi.org/project/discum/)      

# Checklist
- [x] Sending basic text messages
- [X] Sending Images
- [x] Sending Embeds
- [X] Sending Requests (Friends etc)
- [X] Profile Editing (Name,Status,Avatar)
- [X] On-Message (and other on-anything gateway) capabilities
- [X] Getting guild members
- [X] improve documentation
- [X] add interactions (slash command triggering, buttons, and dropdowns/menus)
- [ ] add more guild http api wraps
- [ ] media (voice & video calls, along with the various discord games/activites)
- [ ] Everything

## FAQ
Q: Why am I getting Attribute Errors?          
A: Most likely you've installed discum through pip, which is not always updated. To get the most recent version, install through github. For gateway.session related errors, you need to connect to the gateway at least once to receive session data.    

Q: Does discum support BOT accounts?         
A: No. Discum only supports user accounts.      

Q: What's the difference between user/private API and BOT API?      
A: User APIs are run by the official client. Many of these are not documented by discord. On the other hand, BOT APIs are run by BOT accounts and are documented by discord. Discum only consists of user APIs.    

Q: How to fix "\[SSL: CERTIFICATE_VERIFY_FAILED]" errors?      
A: https://stackoverflow.com/a/53310545/14776493       

Q: I'm getting ```KeyError: 'members'``` when running ```bot.gateway.session.guild(guild_ID).members```. Why?      
A: KeyErrors happened on previous versions where the "members" key was not set until you ran ```bot.gateway.fetchMembers(...); bot.gateway.run()```. Due to this causing some confusion, the latest versions do not display this KeyError (instead, the value of "members" is an empty dictionary to start with). Of course, you still have to fetch the members (a gateway operation) in order to get the members.

Q: ```import _brotli ImportError: DLL load failed: The specified module could not be found.``` How to fix?       
A: https://github.com/google/brotli/issues/782        
     
Q: ```The owner of this website (discord.com) has banned your access based on your browser's signature...```. How to fix?        
A: This is because of your user agent (https://stackoverflow.com/a/24914742/14776493). Either try again or reinitialize your client with a new user agent.       
    
## Notes
In recent years, token logging has become more common (as many people don't check code before they run it). I've seen many closed-source selfbots, and while surely some are well intentioned, others not so much. Discum (discord api wrapper) is open-sourced and organized to provide transparency, but even so, we encourage you to look at the code. Not only will looking at the code help you to better understand how discord's api is structured, but it'll also let you know exactly what you're running. If you have questions about Discum (after looking at the docs & previous issues), free to ask us.

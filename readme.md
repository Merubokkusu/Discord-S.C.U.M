# DisCum
![version](https://img.shields.io/badge/github%20version-1.0.0-blue) [![python versions](https://img.shields.io/badge/python-2.7%20%7C%203.5%20%7C%203.6%20%7C%203.7%20%7C%203.8-blue)](https://github.com/Merubokkusu/Discord-S.C.U.M)       
[![PyPI version](https://badge.fury.io/py/discum.svg)](https://badge.fury.io/py/discum) [![python versions](https://img.shields.io/badge/python-2.7%20%7C%203.5%20%7C%203.6%20%7C%203.7%20%7C%203.8-green)](https://pypi.org/project/discum)      
A simple, easy to use, non-restrictive Discord API Wrapper for Selfbots/Userbots written in Python.       
-using requests and websockets :)

![https://files.catbox.moe/3ns003.png](https://files.catbox.moe/3ns003.png)
        
\* You can send issues to discordtehe@gmail.com (arandomnewaccount will respond). If you put them in the issues tab, either arandomnewaccount will edit your message to "respond" because he can't post public comments or Merubokkusu will respond.

## Table of Contents
- [Key Features](#Key-features)
- [About](#About)
- [Installation](#Installation)
  - [Prerequisites](#prerequisites-installed-automatically-using-above-methods)
- [Example Usage](#Example-usage)
- [Links](#Links)
- [To Do](#To-Do)
- [Contributing](#Contributing)
- [Notes](#Notes)
- [Python 3.9 support?](#39-support)

## Key features
- easy-to-use (make selfbots/userbots)
- easy-to-extend/edit (adding more api wrappers)
- readable (organized 😃 )
- on-event (gateway) capabilities
- ability to fetch guild members (the ones that you can see from the member list)
- support for python 2.7

## About
  Discum is a Discord selfbot api wrapper (in case you didn't know, selfbotting = automating a user account). Whenever you login to discord, your client communicates with Discord's servers using Discord's http api (http(s) requests) and gateway server (websockets). Discum allows you have this communication with Discord with python. 
  
  The main difference between Discum and other Discord api wrapper libraries (like discord.py) is that discum is written and maintained to work on user accounts (so, perfect for selfbots). We thoroughly test all code on here and develop discum to be readable, expandable, and useable.     
  
  Note, using a selfbot is against Discord's Terms of Service and you could get banned for using one if you're not careful. Also, this needs to be said: discum does not have rate limit handling. The main reasons for this are that discum is made to (1) be (relatively) simple and (2) give the developer/user freedom (generally I'd recommend a bit more than 1 second in between tasks of the same type, but if you'd like a longer or shorter wait time that's up to you). We (Merubokkusu and anewrandomaccount) do not take any responsibility for any consequences you might face while using discum. We also do not take any responsibility for any damage caused (to servers/channels) through the use of Discum. Discum is a tool; how you use this tool is on you.

## Installation    
```
git clone https://github.com/Merubokkusu/Discord-S.C.U.M.git
cd Discord-S.C.U.M
python setup.py install               
```
from PyPI:      
```python
pip install discum 
```               
#### Prerequisites (installed automatically using above methods)
- requests
- requests_toolbelt
- websocket_client
- filetype
- ua-parser
- random_user_agent

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
[Documentation](https://github.com/Merubokkusu/Discord-S.C.U.M/tree/master/docs)      
[More examples](https://github.com/Merubokkusu/Discord-S.C.U.M/tree/master/examples)      
[Changelog](https://github.com/Merubokkusu/Discord-S.C.U.M/blob/master/changelog.md)      
[GitHub](https://github.com/Merubokkusu/Discord-S.C.U.M)      
[PyPi](https://pypi.org/project/discum/)      

# To Do
- [x] Sending basic text messages
- [X] Sending Images
- [x] Sending Embeds
- [X] Sending Requests (Friends etc)
- [X] Profile Editing (Name,Status,Avatar)
- [X] On-Message (and other on-anything gateway) capabilities
- [X] Getting guild members
- [ ] Making phone calls, sending audio/video data thru those calls
- [ ] bypass fingerprint detection? maybe?
- [ ] Everything

## Contributing
Contributions are welcome. You can submit issues, make pull requests, or suggest features. Ofc not all suggestions will be implemented (because discum is intended to be a transparent, relatively-raw discord user api wrapper), but all suggestions will be looked into.            

## Notes:
In recent years, token logging has become more common (as many people don't check code before they run it). I've seen many closed-source selfbots, and while surely some are well intentioned, others not so much. Discum (discord api wrapper) is open-sourced and organized to provide transparency, but even so, we encourage you to look at the code. Not only will looking at the code help you to better understand how discord's api is structured, but it'll also let you know exactly what you're running. If you have any questions about Discum, feel free to ask us.

## 3.9 support?
Discum doesn't support python 3.9 because the module we use for websocket connections doesn't support 3.9 yet.       
If you want to use 3.9 with discum, you'll have to either edit your installation of websocket-client as done in [this PR](https://github.com/websocket-client/websocket-client/pull/594) or reinstall websocket-client from [this repo](https://github.com/Flytrex/websocket-client/tree/bugfix/use-is-alive) like this:
```
git clone --branch bugfix/use-is-alive https://github.com/Flytrex/websocket-client.git
cd websocket-client
python setup.py install
```

### A Discord Selfbot Api - discum

![https://files.catbox.moe/3ns003.png](https://files.catbox.moe/3ns003.png)

[![PyPI version](https://badge.fury.io/py/discum.svg)](https://badge.fury.io/py/discum)


## Install
from PyPI:      
```python
pip install discum 
```
     
from source (this is up-to-date with recent changes)(currently on version 0.2.0):        
`git clone https://github.com/Merubokkusu/Discord-S.C.U.M.git`    
`cd Discord-S.C.U.M`     
`python3 setup.py install`            

# Usage
## [Read the Wiki](https://github.com/Merubokkusu/Discord-S.C.U.M/wiki)

# Example
```python
import discum     
bot = discum.Client(email=,password=)
#bot = discum.Client(email=,password=,proxy_host=,proxy_port=)
#bot = discum.Client(token=)
bot.read()
bot.read(update=False).__dict__
bot.getGuildIDs(update=False)
bot.sendMessage("383003333751856129","Hello You :)")
```
# To Do
- [x] Sending basic text messages
- [X] Sending Images
- [x] Sending Embeds
- [X] Sending Requests (Friends etc)
- [X] Profile Editing (Name,Status,Avatar)
- [ ] Making phone calls, sending audio/video data thru those calls
- [ ] Everything

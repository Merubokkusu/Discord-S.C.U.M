### A Discord Selfbot Api - discum

![https://files.catbox.moe/3ns003.png](https://files.catbox.moe/3ns003.png)

[![PyPI version](https://badge.fury.io/py/discum.svg)](https://badge.fury.io/py/discum)


## Install
```python
pip install discum 
```

# Usage

`import discum`      
`bot = discum.Client('Token')`     

### Check if token is vaild
```python
bot.connectionTest()
```
### get message(s)
```getMessage(ChannelID,num=1)```
```python
bot.getMessage("383003333751856129")

### Send Text message
```sendMessage(ChannelID,message,tts=False)```
```python
bot.sendMessage("383003333751856129","Hello You :)")
```
### Send File
```sendFile(channelID,filelocation,isurl=False,message="")```
```python
bot.sendFile("383003333751856129","https://thiscatdoesnotexist.com/",True)
```

# To Do
- [x] Sending basic text messages
- [X] Sending Images
- [ ] Sending Embeds
- [ ] Sending Requests (Friends etc)
- [ ] Everything

# Things That Will Never Be Done
Due to limitations these features will never happen
* User profile edits

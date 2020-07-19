### A Discord Selfbot Api - discum

![https://files.catbox.moe/3ns003.png](https://files.catbox.moe/3ns003.png)

[![PyPI version](https://badge.fury.io/py/discum.svg)](https://badge.fury.io/py/discum)


## Install
from PyPI:      
```python
pip install discum 
```
     
from source (this is up-to-date with recent changes):        
`git clone https://github.com/Merubokkusu/Discord-S.C.U.M.git`    
`cd Discord-S.C.U.M`     
`cd discum` (now you can use python and import discum)   

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
```
### send text message
```sendMessage(ChannelID,message,tts=False)```
```python
bot.sendMessage("383003333751856129","Hello You :)")
```
### send file
```sendFile(channelID,filelocation,isurl=False,message="")```
```python
bot.sendFile("383003333751856129","https://thiscatdoesnotexist.com/",True)
```
### get list of DMs
```getDMs()```
```python
bot.getDMs()
```
### get list of guilds
```getGuilds()```
```python
bot.getGuilds()
```
### get list of relationships
```getRelationships()```
```python
bot.getRelationships()
```
| Relationship Type | description |
| ------ | ------ |
| 1 | friend |
| 2 | block |
| 3 | incoming friend request |
| 4 | outgoing friend request |
### send friend request
```requestFriend()```
```python
bot.requestFriend(ID)
```
### accept friend request
```acceptFriend()```
```python
bot.acceptFriend(ID)
```
### remove friend or unblock user
```removeRelationship()```
```python
bot.removeRelationship(ID)
```
### send friend request
```blockUser()```
```python
bot.blockUser(ID)
```

# To Do
- [x] Sending basic text messages
- [X] Sending Images
- [x] Sending Embeds
- [X] Sending Requests (Friends etc)
- [ ] Everything
- [ ] Update PyPI

# Things That Will Never Be Done
Due to limitations these features will never happen
* User profile edits

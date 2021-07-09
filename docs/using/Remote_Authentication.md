# Remote Authentication actions
__________

##### ```initRA```
initialize bot.ra
```python
bot.initRA()
```

##### ```remoteAuthLogin```
initializes bot.ra and returns bot.ra.run()
```python
bot.remoteAuthLogin('qrcodefile.png')
```
###### Parameters:
-   saveQrCode(Optional[bool/str]) - set as filename if you'd like to set a specific file location for the qr code image

###### Returns:
(token, userData)

### Extra remote authentication info:

#### variables:
```python
self._last_err = None
self.connected = False
self.interval = None
self.key_pair #rsa key pair
self.public_key #public key
self.decryptor #(PKCS1 OAEP, hash algorithm=SHA256) decryptor
self.fingerprint #discord sends this over
self.qr_url = None #https://discordapp.com/ra/{fingerprint}
self.qr_img = None #qr code object (https://pypi.org/project/PyQRCode/)
self.user_data = None #user data, returned from discord after qr code is scanned
self.token = None #token, returned from discord after login request is accepted on phone
```

#### functions:
##### ```ra.command```
adding a function **without** extra parameters to the ra command list:
```python
@bot.ra.command
def myfunction(response):
    pass
```
or
```python
def myfunction(response):
    pass

bot.ra.command(function)
```
or adding a function **with** extra parameters to the ra command list:
```python
def myfunction(response, guild_id, channel_id, log=True):
    if log: print(guild_id, channel_id)

bot.ra.command(
    {
        "function": myfunction,
        "priority": 0,
        "params": {"guild_id": "123123123", "channel_id": "321321321", "log": True},
    }
)
```
###### Parameters:
- function (function/dict) - function if no extra params needed, dict if extra params needed.       
  Dict version also allows you to specify a priority (optional) where 0 indicates top priority and -1 indicates lowest priority. Think of priority as a command list index.

##### ```ra.removeCommand```
```python
bot.ra.removeCommand(myfunction)
```
###### Parameters:
- function (function/dict) - the function you want to remove
- exactMatch (bool) - only useful if a dict is passed as the function. Will only look for exact dictionary matches if set to True. Else, it will just look for function matches. Defaults to True
- allMatches (bool) - if set to False, only the first match will be removed. Defaults to False

##### ```ra.clearCommands```
```python
bot.ra.clearCommands()
```
##### ```ra.run```
```python
bot.ra.run()
```
###### Parameters:
- saveQrCode(Optional[bool/str]) - set as filename if you'd like to set a specific file location for the qr code image

###### Returns:
(token, userData)

##### ```ra.send```
Send info (in dictionary format) to the remote authentication gateway. It's unlikely that you'll use this since discum automatically handles the handshake.

##### ```ra.close```
```python
@bot.ra.command
def test(response):
    bot.ra.close()
```
##### ```ra.resetSession```
Discum automatically runs this when running ra.run.
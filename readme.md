### A Discord Selfbot Api - discum
![https://files.catbox.moe/3ns003.png](https://files.catbox.moe/3ns003.png)


# Usage

### Send Text message
```sendMessage(Channel ID,Message)```
```python
import discum
bot = discum.Client('Token')
bot.sendMessage("383003333751856129","Hello You :)")
```


### Check if token is vaild
```python
import discum
bot = discum.Client('Token')
bot.connectionTest()
```

# To Do
- [x] Sending basic text messages
- [ ] Sending Images
- [ ] Sending Embeds
- [ ] Sending Requests (Friends etc)

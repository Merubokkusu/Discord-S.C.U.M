# Extending Discum
How to add extra API wraps to discum?
# Table of Contents
- [http APIs](#http-APIs) 
- [gateway APIs](#gateway-APIs)

### http APIs:
There are 2 parts to this: (1) writing the wrapper and (2) wrapping that wrapper. The second part is simply for naming and organization purposes.
Currently, the guild, messages, user folders contain the wrappers. For example, the wrapper for the createDM function can be placed in the messages.py file in the messages folder.

##### 1) The wrapper is coded. 
Here's the format of each type of wrapper (depends on type of http request):

###### GET: 
```python
def wrapper(**params):
    url = "url"
    if self.log: Logger.LogMessage('Get -> {}'.format(url))
    response = self.s.get(url)
    if self.log: Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
    return response
```
###### POST: 
```python
def wrapper(**params):
    url = "url"
    body = {"something": something, ...}
    if self.log: Logger.LogMessage('Post -> {}'.format(url))
    if self.log: Logger.LogMessage('{}'.format(str(body)))
    response = self.s.post(url, data=json.dumps(body))
    if self.log: Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
    return response
```
###### PUT: 
```python
def wrapper(**params):
    url = "url"
    body = {"something": something, ...}
    if self.log: Logger.LogMessage('Put -> {}'.format(url))
    if self.log: Logger.LogMessage('{}'.format(str(body)))
    response = self.s.put(url, data=json.dumps(body))
    if self.log: Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
    return response
```
###### PATCH: 
```python
def wrapper(**params):
    url = "url"
    body = {"something": something, ...}
    if self.log: Logger.LogMessage('Patch -> {}'.format(url))
    if self.log: Logger.LogMessage('{}'.format(str(body)))
    response = self.s.patch(url, data=json.dumps(body))
    if self.log: Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
    return response
```
###### DELETE: 
```python
def wrapper(**params):
    url = "url"
    body = {"something": something, ...}
    if self.log: Logger.LogMessage('Delete -> {}'.format(url))
    response = self.s.delete(url)
    if self.log: Logger.LogMessage('Response <- {}'.format(response.text), log_level=LogLevel.OK)
    return response
```

##### 2) The wrapper is wrapped. This happens in the discum.py file. For example, for the createDM function, the wrapped wrapper looks like this:
```python
def createDM(self,recipients):
    return Messages(self.discord,self.s,self.log).createDM(recipients)
```
self.discord is the discord url (https://discord.com/api/v8/)
self.s is your current client's requests session
self.log tells the discum whether or not to log stuff
### gateway APIs
The gateway functions (located in the gateway folder) are structured in a somewhat similar matter. The main difference is that combo wrappers (functions that use a combination of request functions and parse functions) are located in gateway.py. Request wrappers are in the request.py file and parse wrappers are in the parse.py file.
Functions are organized into dms, guild, media, messages, and user folders. In each folder are 4 files: \_\_init__.py, combo.py, parse.py, and request.py.
##### 1) The wrapper is coded.
The 3 types of wrappers are request, parse, and combo.
###### request:
here's an example of a request wrapper (from discum > gateway > guild > request.py)
```python
def searchGuildMembers(self, guild_ids, query, limit=10, presences=True):
    if isinstance(guild_ids, str):
        guild_ids = [guild_ids]
    self.gatewayobject.send({"op":self.gatewayobject.OPCODE.REQUEST_GUILD_MEMBERS,"d":{"guild_id":guildIDs,"query":query,"limit":limit,"presences":presences}})
```
The only required part of these functions is the ```self.gatewayobject.send``` part. This sends messages to discum thru the gateway.
###### parse
here's an example of a parse function (from discum > gateway > messages > parse.py)
```python
@staticmethod
def message_create(response):
    message = response["d"]
    types = [
        "default",
        "recipient_added",
        "recipient_removed",
        "call",
        "channel_name_changed",
        "channel_icon_changed",
        "channel_message_pinned",
        "guild_member_joined",
        "user_premium_guild_subscription",
        "user_premium_guild_subscription_tier_1",
        "user_premium_guild_subscription_tier_2",
        "user_premium_guild_subscription_tier_3",
        "channel_follow_added",
        "guild_discovery_disqualified",
        "guild_discovery_requalified",
        "reply",
        "application_command"
    ]
    message["type"] = types[response["d"]["type"]] #number to str
    return message
```
Function names are just lowercase types, so for type GUILD_MEMBER_LIST_UPDATE, the function is named guild_member_list_update.
The other required parts are that (1) the method is static (unless you choose to make an \_\_init__ function), (2) response is always the first parameter, and (3) the function returns something.
###### combo
Combo functions such as the fetchMembers function in discum > gateway > guild > combo.py tend to use both request wrappers and parse wrappers. fetchMembers also parses more than 1 response and removes itself from the command list once it finishes fetching members. For a simple example of this automatically-self-removing command, see https://github.com/Merubokkusu/Discord-S.C.U.M/blob/master/discum/gateway/guild/combo.py#L133.
##### 2) The wrapper is wrapped.
###### parse
This happens in the gateway/parse.py file.
Example:
```python
def guild_member_list_update(self):
    return GuildParse.guild_member_list_update(self.response)
```
###### request
This happens in the gateway/request.py file.
Example:
```python
def lazyGuild(self, guild_id, channel_ranges, typing=None, threads=None, activities=None, members=None):
    GuildRequest(self.gatewayobject).lazyGuild(guild_id, channel_ranges, typing, threads, activities, members)
```
###### combo
This happens in the gateway/gateway.py file (at the bottom).
Example:
```python
def testfuncPOG(self, pog):
    self.command({'function': Guild(self).testfuncPOG, 'priority': 0, 'params': {'pog': pog}})
```
You can also place other helper functions at the bottom of gateway/gateway.py, such as the finishedMemberFetching function.
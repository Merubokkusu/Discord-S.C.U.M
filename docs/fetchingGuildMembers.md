# Fetching Guild Members
Alright so this really needs a page of its own because it's special. There's no actual api endpoint to get the guild members, so instead what discum does is fetch the member list, piece by piece. Discum also provides some params for the fetchMembers function that allows you to modify fetching behavior (in almost any way you want).
# Links/Table of Contents
- [Usage](https://github.com/Merubokkusu/Discord-S.C.U.M/blob/master/docs/using.md#fetch-guild-members)
- [Reasoning/Make your own fetchMembers function](https://arandomnewaccount.gitlab.io/discord-unofficial-docs/lazy_guilds.html)
- [What happens when fetchMembers is run](#what-happens)
- [Calculating # of fetchable members]()
- [Examples](#examples)
- [Efficiency & Effectiveness](#efficiency--effectiveness)

### what happens:
1) the member-fetching tracker for that particular guild gets reset
2) the [fetchMembers combo function](https://github.com/Merubokkusu/Discord-S.C.U.M/blob/37a4c66713aac5111fa5fe14aebb866197cf2877/discum/gateway/guild/combo.py#L67) gets inserted at position 0 (or whatever priority you select) in the gateway command list
3) the fetchMembers combo function starts running once ready_supplemental has been received
4) the fetchMembers combo function removes itself from the command list once finished

### calculating # of fetchable members
Even though it's not yet known how discord calculates this, you can still come up with a "ground truth" number. The steps are as follows:
1) open your browser's dev tools (chrome dev tools is a favorite)
2) click on the network tab and make sure you can see websocket connections
3) go to a guild and scroll all the way down on the member list
4) see what are the ranges of the last gateway request your client sends (the # of fetchable members is somewhere in these ranges)

### examples

This first example runs the fetchMembers function while the gateway is running (both examples below use the "overlap" method):
```python
import discum
bot = discum.Client(token='ur token')

@bot.gateway.command
def memberTest(resp):
	guild_id = '322850917248663552'
	channel_id = '754536220826009670'
	if resp.event.ready_supplemental:
		bot.gateway.fetchMembers(guild_id, channel_id)
	if bot.gateway.finishedMemberFetching(guild_id):
		lenmembersfetched = len(bot.gateway.session.guild(guild_id).members)
		print(str(lenmembersfetched)+' members fetched')
		bot.gateway.removeCommand(memberTest)
		bot.gateway.close()

bot.gateway.run()

for memberID in bot.gateway.session.guild('322850917248663552').members:
	print(memberID)
```
And this second example runs fetchMembers before the gateway is run:
```python
import discum
bot = discum.Client(token='ur token')
guild_id = '322850917248663552'
channel_id = '754536220826009670'
bot.gateway.fetchMembers(guild_id, channel_id)
@bot.gateway.command
def memberTest(resp):
	if bot.gateway.finishedMemberFetching('322850917248663552'):
		lenmembersfetched = len(bot.gateway.session.guild('322850917248663552').members)
		print(str(lenmembersfetched)+' members fetched')
		bot.gateway.removeCommand(memberTest)
		bot.gateway.close()

bot.gateway.run()

for memberID in bot.gateway.session.guild('322850917248663552').members:
	print(memberID)
```
It's possible that fetchMembers doesn't fetch all fetchable members. Don't worry if this happens, you can start fetching members from any index. (discum calculates ranges using index x multiplier, the multiplier used below is 100):
```python
#import discum
#bot = discum.Client(token='ur token')
guild_id = '322850917248663552'
channel_id = '754536220826009670'
bot.gateway.fetchMembers(guild_id, channel_id, method="overlap", indexStart=50, reset=False) #overlap method means multiplier is 100, reset is False because you want to keep previous data
@bot.gateway.command
def memberTest(resp):
	if bot.gateway.finishedMemberFetching('322850917248663552'):
		lenmembersfetched = len(bot.gateway.session.guild('322850917248663552').members)
		print(str(lenmembersfetched)+' members fetched')
		bot.gateway.removeCommand(memberTest)
		bot.gateway.close()

bot.gateway.run()

for memberID in bot.gateway.session.guild('322850917248663552').members:
	print(memberID)
```

# Efficiency & Effectiveness
Alright so technically there are 2 ways to get the member list. The first way is through websockets (which is what discum uses). The second way is through html scraping (which I don't recommend since I imagine that'd be slower).
  
Using a slightly-modified version of discum (just 6 lines extra to track times and member counts), these stats were collected on discum's fetchMembers's efficiency and effectiveness:

|      | overlap&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; | no overlap |
|------|---------|------------|
| 2.1k |![a](https://raw.githubusercontent.com/Merubokkusu/Discord-S.C.U.M/master/docs/memberFetchingStats/2100a.jpg)    |![c](https://raw.githubusercontent.com/Merubokkusu/Discord-S.C.U.M/master/docs/memberFetchingStats/2100b.jpg)       |
| 128k |![b](https://raw.githubusercontent.com/Merubokkusu/Discord-S.C.U.M/master/docs/memberFetchingStats/128ka.jpg)    |![d](https://raw.githubusercontent.com/Merubokkusu/Discord-S.C.U.M/master/docs/memberFetchingStats/128kb.jpg)       |
###### \* the bottom right picture says "128 fetchable"; it's supposed to say "128k fetchable"

As you can see, the "no overlap" method fetches 200 members/second while the "overlap" method fetches 100 members/second. However, "no overlap" is also a lot less effective. After doing a few more tests with both methods ("overlap" and "no overlap"), "no overlap" shows a lot less consistency/reliability than "overlap".

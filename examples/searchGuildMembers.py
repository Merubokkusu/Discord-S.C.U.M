#search guild members aka opcode 8 aka replacement for bot.getGuildMember()

#EXAMPLE 1: query member search in guild(s)
@bot.gateway.command
def test(resp):
    if resp.event.ready_supplemental:
        bot.gateway.queryGuildMembers(['guildID'], 'a', limit=100, keep="all")
    if resp.event.guild_members_chunk and bot.gateway.finishedGuildSearch(['guildID'], 'a'):
        bot.gateway.close()

bot.gateway.run()

print(bot.gateway.guildMemberSearches['guildID']['queries']['a']) #user IDs of results
print(bot.gateway.session.guild('guildID').members) #member data
bot.gateway.clearCommands()

#EXAMPLE 2: search for userID(s) in guild(s)
@bot.gateway.command
def test(resp):
    if resp.event.ready_supplemental:
        bot.gateway.checkGuildMembers(['guildID'], ['userID1', 'userID2'], keep="all")
    if resp.event.guild_members_chunk and bot.gateway.finishedGuildSearch(['guildID'], userIDs=['userID1', 'userID2']):
        bot.gateway.close()

bot.gateway.run()

print(bot.gateway.guildMemberSearches['guildID']['ids']) #user IDs of results
print(bot.gateway.session.guild('guildID').members) #member data
bot.gateway.clearCommands()

#EXAMPLE 3: opcode 8 brute forcer
#not entirely random. Optimized quite a bit.

import time
import re

allchars = [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~']
bot.gateway.guildMemberSearches = {}
bot.gateway.resetMembersOnSessionReconnect = False #member list brute forcing can take a while

class Queries:
    qList = ["!"] #query list

class MemberFetchingScore:
    def __init__(self, perRequestExpectation, perSecondExpectation):
        self.perRequestExpectation = perRequestExpectation #expected # of members per request
        self.perSecondExpectation = perSecondExpectation #expected # of members per second
        self.effectiveness = 0
        self.efficiency = 0
        self.completeness = 0
    #percentage of requests returning back expected # of members
    def calculateEffectiveness(self, guildID):
        self.effectiveness = 100*(len(bot.gateway.session.guild(guildID).members)/len(bot.gateway.guildMemberSearches[guildID]["queries"]))/self.perRequestExpectation
    #percentage of expected members fetched per second
    def calculateEfficiency(self, guildID, startTime):
        totalTime = time.time() - startTime
        self.efficiency = 100*(len(bot.gateway.session.guild(guildID).members)/totalTime)/self.perSecondExpectation
    #percentage of members fetched over total members in server
    def calculateCompleteness(self, guildID):
        self.completeness = 100*(len(bot.gateway.session.guild(guildID).members)/bot.gateway.session.guild(guildID).memberCount)
    #average of measures, 0<=score<=100
    def getScore(self):
        return (self.effectiveness+self.efficiency+self.completeness)/3

s = MemberFetchingScore(100, 100)

def calculateOption(guildID, action): #action == 'append' or 'replace'
    if action == 'append':
        lastUserIDs = bot.gateway.guildMemberSearches[guildID]["queries"][''.join(Queries.qList)]
        data = [bot.gateway.session.guild(guildID).members[i] for i in bot.gateway.session.guild(guildID).members if i in lastUserIDs]
        lastName = sorted(set([re.sub(' +', ' ', j['nick'].lower()) if (j.get('nick') and re.sub(' +', ' ', j.get('nick').lower()).startswith(''.join(Queries.qList))) else re.sub(' +', ' ', j['username'].lower()) for j in data]))[-1]
        try:
            option = lastName[len(Queries.qList)]
            return option
        except IndexError:
            return None
    elif action == 'replace':
        if Queries.qList[-1] in allchars:
            options = allchars[allchars.index(Queries.qList[-1])+1:]
            if ' ' in options and (len(Queries.qList)==1 or (len(Queries.qList)>1 and Queries.qList[-2]==' ')): #cannot start with a space and cannot have duplicate spaces
                options.remove(' ')
            return options
        else:
            return None

def findReplaceableIndex(guildID):
    for i in range(len(Queries.qList)-2, -1, -1): #assume that the last index is not changable
        if Queries.qList[i] != '~':
            return i
    return None

def bruteForceTest(resp, guildID, wait):
    if resp.event.ready_supplemental:
        s.startTime = time.time()
        bot.gateway.queryGuildMembers([guildID], query=''.join(Queries.qList), limit=100, keep="all")
    elif resp.event.guild_members_chunk:
        remove = False
        if len(bot.gateway.guildMemberSearches[guildID]["queries"][''.join(Queries.qList)]) == 100: #append
            appendOption = calculateOption(guildID, 'append')
            if appendOption:
                Queries.qList.append(appendOption)
            else:
                remove = True
        else: #if <100 results returned, replace
            replaceOptions = calculateOption(guildID, 'replace')
            if replaceOptions:
                Queries.qList[-1] = replaceOptions[0]
            else:
                remove = True
        if remove: #if no replace options, find first replaceable index & replace it
            if len(Queries.qList) == 1: #reached end of possibilities
                bot.gateway.removeCommand({"function": bruteForceTest, "params":{"guildID":guildID, "wait":wait}})
                s.calculateEfficiency(guildID, s.startTime)
                print("efficiency: "+repr(s.efficiency)+"%")
                s.calculateCompleteness(guildID)
                print("completeness: "+repr(s.completeness)+"%")
                print("score: "+repr(s.getScore()))
                bot.gateway.close()
            else:
                replaceableInd = findReplaceableIndex(guildID)
                if replaceableInd != None:
                    Queries.qList = Queries.qList[:replaceableInd+1]
                    replaceOptions = calculateOption(guildID, 'replace')
                    Queries.qList[-1] = replaceOptions[0]
                else:
                    bot.gateway.removeCommand({"function": bruteForceTest, "params":{"guildID":guildID, "wait":wait}})
                    s.calculateEfficiency(guildID, s.startTime)
                    print("efficiency: "+repr(s.efficiency)+"%")
                    s.calculateCompleteness(guildID)
                    print("completeness: "+repr(s.completeness)+"%")
                    print("score: "+repr(s.getScore()))
                    bot.gateway.close()
        if wait: time.sleep(wait)
        print("next query: "+"".join(Queries.qList))
        print("members fetched so far: "+repr(len(bot.gateway.session.guild(guildID).members)))
        s.calculateEffectiveness(guildID)
        print("effectiveness: "+repr(s.effectiveness)+"%")
        bot.gateway.queryGuildMembers([guildID], query=''.join(Queries.qList), limit=100, keep="all")


guildID = ''
wait = 1
bot.gateway.command({"function": bruteForceTest, "params":{"guildID":guildID, "wait":wait}})
bot.gateway.run()

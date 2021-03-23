import websocket
import json
import time
import random
import base64
import zlib
import copy

#some http wraps that help gateway functions:
from ..user.user import User

if __import__('sys').version.split(' ')[0] < '3.0.0':
    import thread
else:
    import _thread as thread

from .session import Session
from .response import Resp
from .request import Request

from .parse import Parse

#other functions
from .guild.combo import GuildCombo
from .user.combo import UserCombo

#exceptions
class InvalidSessionException(Exception):
    pass

class ConnectionManuallyClosedException(Exception):
	pass

def exceptionChecker(e, types, andOr="OR"):
	if andOr=="AND":
		for i in types:
			if not isinstance(e,i):
				return False
		return True
	elif andOr=="OR":
		for i in types:
			if isinstance(e,i):
				return True
		return False

#gateway class
class GatewayServer:

    class LogLevel:
        SEND = '\033[94m'
        RECEIVE = '\033[92m'
        WARNING = '\033[93m'
        DEFAULT = '\033[m'

    class OPCODE:
        # Name                           Code    Client Action   Description
        DISPATCH =                       0  #    Receive         dispatches an event
        HEARTBEAT =                      1  #    Send/Receive    used for ping checking
        IDENTIFY =                       2  #    Send            used for client handshake
        PRESENCE_UPDATE =                3  #    Send            used to update the client status
        VOICE_STATE_UPDATE =             4  #    Send            used to join/move/leave voice channels
        VOICE_SERVER_PING =              5  #    Send            used for voice ping checking
        RESUME =                         6  #    Send            used to resume a closed connection
        RECONNECT =                      7  #    Receive         used to tell bots to reconnect...so..useless for discum
        REQUEST_GUILD_MEMBERS =          8  #    Send            used to request guild members (when searching for members in the search bar of a guild)
        INVALID_SESSION =                9  #    Receive         used to notify client they have an invalid session id
        HELLO =                          10 #    Receive         sent immediately after connecting, contains heartbeat and server debug information
        HEARTBEAT_ACK =                  11 #    Sent immediately following a client heartbeat that was received
        #GUILD_SYNC =                    12 #    Receive         supposedly guild_sync but not used...idk
        DM_UPDATE =                      13 #    Send            used to get dm features
        LAZY_REQUEST =                   14 #    Send            discord responds back with GUILD_MEMBER_LIST_UPDATE type SYNC...
        LOBBY_CONNECT =                  15 #    ??
        LOBBY_DISCONNECT =               16 #    ??
        LOBBY_VOICE_STATES_UPDATE =      17 #    Receive
        STREAM_CREATE =                  18 #    ??
        STREAM_DELETE =                  19 #    ??
        STREAM_WATCH =                   20 #    ??
        STREAM_PING =                    21 #    Send
        STREAM_SET_PAUSED =              22 #    ??
        REQUEST_APPLICATION_COMMANDS =   24 #    ??

    def __init__(self, websocketurl, token, super_properties, sessionobj="", RESTurl="", log=True): #session obj needed for proxies and some combo gateway functions (that also require http api wraps)
        self.token = token
        self.super_properties = super_properties
        self.auth = {
                "token": self.token,
                "capabilities": 61,
                "properties": self.super_properties,
                "presence": {
                    "status": "online",
                    "since": 0,
                    "activities": [],
                    "afk": False
                },
                "compress": False,
                "client_state": {
                    "guild_hashes": {},
                    "highest_last_message_id": "0",
                    "read_state_version": 0,
                    "user_guild_settings_version": -1
                }
            }
        self.RESTurl = RESTurl #for helper http requests
        self.sessionobj = sessionobj #for helper http requests

        self.proxy_host = None if "https" not in sessionobj.proxies else sessionobj.proxies["https"][8:].split(":")[0]
        self.proxy_port = None if "https" not in sessionobj.proxies else sessionobj.proxies["https"][8:].split(":")[1]

        self.keepData = ("dms", "guilds", "guild_channels")
        self.log = log

        self.interval = None
        self.session_id = None
        self.sequence = 0
        self.READY = False #becomes True once READY_SUPPLEMENTAL is received
        self.session = Session({},{})

        #websocket.enableTrace(True) #for debugging
        self.ws = self._get_ws_app(websocketurl)

        self._after_message_hooks = []
        self._last_err = None

        self.connected = False
        self.resumable = False

        self.voice_data = {} #voice connections dependent on current (connected) session

        self.memberFetchingStatus = {"first": []}

        self.request = Request(self)
        self.parse = Parse

    #WebSocketApp, more info here: https://github.com/websocket-client/websocket-client/blob/master/websocket/_app.py#L79
    def _get_ws_app(self, websocketurl):
        sec_websocket_key = base64.b64encode(bytes(random.getrandbits(8) for _ in range(16))).decode() #https://websockets.readthedocs.io/en/stable/_modules/websockets/handshake.html
        headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "Upgrade",
            "Host": "gateway.discord.gg",
            "Origin": "https://discord.com",
            "Pragma": "no-cache",
            "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
            "Sec-WebSocket-Key": sec_websocket_key,
            "Sec-WebSocket-Version": "13",
            "Upgrade": "websocket",
            "User-Agent": self.super_properties["browser_user_agent"]
        } #more info: https://stackoverflow.com/a/40675547

        ws = websocket.WebSocketApp(websocketurl,
                                    header = headers,
                                    on_open=lambda ws: self.on_open(ws),
                                    on_message=lambda ws, msg: self.on_message(ws, msg),
                                    on_error=lambda ws, msg: self.on_error(ws, msg),
                                    on_close=lambda ws: self.on_close(ws)
                                    )
        return ws

    def decompress(self, bmessage): #input is byte message
        data = self._zlib.decompress(bmessage)
        jsonmessage = json.loads(data.decode("UTF8"))
        return jsonmessage

    def on_open(self, ws):
        self.connected = True
        self.memberFetchingStatus = {"first": []}
        if self.log: print("Connected to websocket.")
        if not self.resumable:
            self.send({"op": self.OPCODE.IDENTIFY, "d": self.auth})
        else:
            self.resumable = False
            self.send({"op": self.OPCODE.RESUME, "d": {"token": self.token, "session_id": self.session_id, "seq": self.sequence-1 if self.sequence>0 else self.sequence}})

    def on_message(self, ws, message):
        self.sequence += 1
        response = self.decompress(message)
        resp = Resp(copy.deepcopy(response))
        if self.log: print('%s< %s%s' % (self.LogLevel.RECEIVE, response, self.LogLevel.DEFAULT))
        if response['op'] == self.OPCODE.HELLO: #only happens once, first message sent to client
            self.interval = (response["d"]["heartbeat_interval"])/1000 #if this fails make an issue and I'll revert it back to the old method (slightly smaller wait time than heartbeat)
            thread.start_new_thread(self._heartbeat, ())
        elif response['op'] == self.OPCODE.INVALID_SESSION:
            if self.log: print("Invalid session.")
            self._last_err = InvalidSessionException("Invalid Session Error.")
            if self.resumable:
                self.resumable = False
                self.sequence = 0
                self.close()
            else:
                self.sequence = 0
                self.close()
        if self.interval == None:
            if self.log: print("Identify failed.")
            self.close()
        if resp.event.ready:
            self._last_err = None
            self.session_id = response['d']['session_id']
            self.settings_ready = resp.parsed.ready() #parsed
            self.session = Session(self.settings_ready, {})
        elif resp.event.ready_supplemental:
            self.resumable = True #completely successful identify
            self.settings_ready_supp = resp.parsed.ready_supplemental() #parsed
            self.session = Session(self.settings_ready, self.settings_ready_supp) #reinitialize i guess
            self.READY = True
        self.sessionUpdates(resp)
        thread.start_new_thread(self._response_loop, (resp,))

    def on_error(self, ws, error):
        if self.log: print('%s%s%s' % (self.LogLevel.WARNING, error, self.LogLevel.DEFAULT))
        self._last_err = error

    def on_close(self, ws):
        self.connected = False
        self.READY = False #reset self.READY
        if self.log: print('websocket closed')

    #Discord needs heartbeats, or else connection will sever
    def _heartbeat(self):
        if self.log: print("entering heartbeat")
        while self.connected:
            time.sleep(self.interval)
            if not self.connected:
                break
            self.send({"op": self.OPCODE.HEARTBEAT,"d": self.sequence-1 if self.sequence>0 else self.sequence})

    #just a wrapper for ws.send
    def send(self, payload):
        if self.log: print('%s> %s%s' % (self.LogLevel.SEND, payload, self.LogLevel.DEFAULT))
        self.ws.send(json.dumps(payload))

    def close(self):
        self.connected = False
        self.READY = False #reset self.READY
        if not isinstance(self._last_err, InvalidSessionException):
        	self._last_err = ConnectionManuallyClosedException("Disconnection initiated by client using close function.")
        if self.log: print('websocket closed') #don't worry if this message prints twice
        self.ws.close()

    def command(self, func):
        if callable(func):
            self._after_message_hooks.append(func)
            return func
        elif isinstance(func, dict): #because I can't figure out out to neatly pass params to decorators :(. Normal behavior still works; use as usual.
            priority = func.pop('priority', len(self._after_message_hooks))
            self._after_message_hooks.insert(priority, func)
            return func['function']

    #kinda influenced by https://github.com/scrubjay55/Reddit_ChatBot_Python/blob/master/Reddit_ChatBot_Python/WebSockClient.py (Apache License 2.0)
    def _response_loop(self, resp):
        commandslist = self._after_message_hooks[:] #create a copy
        for func in commandslist:
            if callable(func):
                func(resp)
            elif isinstance(func, dict):
                function = func['function']
                params = func['params'] if 'params' in func else {}
                function(resp, **params)

    def removeCommand(self, func, exactMatch=True, allMatches=False):
        try:
            if exactMatch:
                self._after_message_hooks.index(func) #for raising the value error
                if allMatches:
                    self._after_message_hooks = [i for i in self._after_message_hooks if i!=func]
                else: #simply remove first found
                    del self._after_message_hooks[self._after_message_hooks.index(func)]
            else:
                commandsCopy = [i if callable(i) else i['function'] for i in self._after_message_hooks] #list of just functions
                commandsCopy.index(func) #for raising the value error
                if allMatches:
                    self._after_message_hooks = [i for (i,j) in zip(self._after_message_hooks, commandsCopy) if j!=func]
                else:
                    del self._after_message_hooks[commandsCopy.index(func)]
        except ValueError:
            if self.log: print('%s not found in _after_message_hooks.' % func)
            pass

    def clearCommands(self):
        self._after_message_hooks = []

    def resetSession(self): #just resets some variables that in-turn, resets the session (client side). Do not run this while running run().
        self.interval = None
        self.session_id = None
        self.sequence = 0
        self.READY = False #becomes True once READY_SUPPLEMENTAL is received
        self._last_err = None
        self.voice_data = {}
        self.resumable = False #you can't resume anyways without session_id and sequence

    #modified version of function run_4ever from https://github.com/scrubjay55/Reddit_ChatBot_Python/blob/master/Reddit_ChatBot_Python/Utils/WebSockClient.py (Apache License 2.0)
    def run(self, auto_reconnect=True):
        try:
            self._zlib = zlib.decompressobj()
            self.ws.run_forever(ping_interval=10, ping_timeout=5, http_proxy_host=self.proxy_host, http_proxy_port=self.proxy_port)
            raise self._last_err
        except KeyboardInterrupt:
            self._last_err = KeyboardInterrupt("Keyboard Interrupt Error")
            if self.log: print("Connection forcibly closed using Keyboard Interrupt.")
            assert True
        except Exception as e:
            if auto_reconnect:
                if not exceptionChecker(e, [KeyboardInterrupt]):
                    if exceptionChecker(e, [websocket._exceptions.WebSocketAddressException, websocket._exceptions.WebSocketTimeoutException], "OR"):
                        self._last_err = None
                        waitTime = random.randrange(1,6)
                        if self.log: print("Connection Dropped. Attempting to resume last valid session in %s seconds." % waitTime)
                        time.sleep(waitTime)
                        self.run()
                    elif not exceptionChecker(e, [ConnectionManuallyClosedException]):
                        self.resetSession()
                        if self.log: print("Connection Dropped. Retrying in 10 seconds.")
                        time.sleep(10)
                        self.run()
                    else:
                        if self.log: print("Connection forcibly closed using close function.")
            else:
            	pass

    ######################################################
    def sessionUpdates(self, resp):
        #***guilds
        #guild created
        if resp.event.guild:
            guildData = resp.parsed.guild_create(my_user_id=self.session.user['id']) #user id needed for updating personal roles in that guild
            guildID = guildData['id']
            voiceStateData = guildData.pop('voice_states', [])
            self.session.setGuildData(guildID, guildData)
            self.session.setVoiceStateData(guildID, voiceStateData)
        #guild deleted
        elif resp.event.guild_deleted:
            if "guilds" in self.keepData:
                self.session.guild(resp.raw['d']['id']).updateData({"removed": True})  #add the indicator
            else:
                self.session.removeGuildData(resp.raw['d']['id'])

        #***channels (dms and guilds)
        #channel created (either dm or guild channel)
        elif resp.event.channel:
            channelData = resp.parsed.channel_create()
            channelID = channelData['id']
            if channelData["type"] in ("dm", "group_dm"): #dm
                self.session.setDmData(channelID, channelData)
            else: #other channels
                guildID = channelData.pop("guild_id")
                self.session.guild(guildID).setChannelData(channelID, channelData)
        #channel deleted (either dm or guild channel)
        elif resp.event.channel_deleted:
            channelData = resp.parsed.channel_delete() #updated data :) ...unlike guild_delete events
            channelData["removed"] = True #add the indicator
            channelID = channelData["id"]
            if channelData["type"] in ("dm", "group_dm"): #dm
                if "dms" in self.keepData:
                    self.session.DM(channelID).updateData(channelData)
                else:
                    self.session.removeDmData(channelID)
            else: #other channels (guild channels)
                guildID = channelData.pop("guild_id")
                if "guild_channels" in self.keepData:
                    self.session.guild(guildID).updateChannelData(channelID, channelData)
                else:
                    self.session.guild(guildID).removeChannelData(channelID)

        #***user updates
        #user settings updated
        elif resp.event.settings_updated:
            self.session.updateUserSettings(resp.raw['d'])
        #user session replaced (useful for syncing activities btwn client and server)
        elif resp.event.session_replaced:
            newStatus = resp.parsed.sessions_replace(session_id=self.session_id) #contains both status and activities
            self.session.updateUserSettings(newStatus)
    ######################################################

    '''
    Guild/Server stuff
    '''
    def getMemberFetchingParams(self, targetRangeStarts): #more for just proof of concept. targetRangeStarts must not contain duplicates and must be a list of integers
        targetRangeStarts = {i:1 for i in targetRangeStarts} #remove duplicates but preserve order
        if targetRangeStarts.get(0)!=None and targetRangeStarts.get(100)!=None:
            keys = list(targetRangeStarts)
            if keys.index(100)<keys.index(0):
                targetRangeStarts.pop(0) #needs to be removed or else fetchMembers will enter an infinite loop because of how discord responds to member list requests
        startIndex = 1 #can't start at 0 because can't divide by 0. No need to specify a stop index since fetchMembers continues until end of multipliers
        method = [0] #because startIndex is 1
        for index,i in enumerate(targetRangeStarts):
            method.append(i/(index+1))
        return startIndex, method #return startIndex and multipliers

    def fetchMembers(self, guild_id, channel_id, method="overlap", keep=[], considerUpdates=True, startIndex=0, stopIndex=1000000000, reset=True, wait=None, priority=0):
        if guild_id in self.memberFetchingStatus:
            del self.memberFetchingStatus[guild_id] #just resetting tracker on the specific guild_id
        self.command(
            {
                "function": GuildCombo(self).fetchMembers,
                "priority": priority,
                "params": {
                    "guild_id": guild_id,
                    "channel_id": channel_id,
                    "method": method,
                    "keep": keep,
                    "considerUpdates": considerUpdates,
                    "startIndex": startIndex,
                    "stopIndex": stopIndex,
                    "reset": reset,
                    "wait": wait
                },
            }
        )


    def finishedMemberFetching(self, guild_id):
        return self.memberFetchingStatus.get(guild_id) == "done"


    '''
    User stuff
    '''
    def setStatus(self, status): #can only be run while connected to gateway
        User(self.RESTurl,self.sessionobj,self.log).setStatusHelper(status, timeout=0.02)
        UserCombo(self).setStatus(status)

    def setPlayingStatus(self, game): #can only be run while connected to gateway, will update metadata later
        if not self.session.userSettings['show_current_game']:
            User(self.RESTurl,self.sessionobj,self.log).enableActivityDisplay(enable=True, timeout=0.02)
        UserCombo(self).setPlayingStatus(game)

    def removePlayingStatus(self): #can only be run while connected to gateway
        UserCombo(self).removePlayingStatus()

    def setStreamingStatus(self, stream, url): #can only be run while connected to gateway, will update metadata later
        if not self.session.userSettings['show_current_game']:
            User(self.RESTurl,self.sessionobj,self.log).enableActivityDisplay(enable=True, timeout=0.02)
        UserCombo(self).setStreamingStatus(stream, url)

    def removeStreamingStatus(self): #can only be run while connected to gateway
        UserCombo(self).removeStreamingStatus()

    def setListeningStatus(self, song): #can only be run while connected to gateway, will update metadata later
        if not self.session.userSettings['show_current_game']:
            User(self.RESTurl,self.sessionobj,self.log).enableActivityDisplay(enable=True, timeout=0.02)
        UserCombo(self).setListeningStatus(song)

    def removeListeningStatus(self): #can only be run while connected to gateway
        UserCombo(self).removeListeningStatus()

    def setWatchingStatus(self, show): #can only be run while connected to gateway, will update metadata later
        if not self.session.userSettings['show_current_game']:
            User(self.RESTurl,self.sessionobj,self.log).enableActivityDisplay(enable=True, timeout=0.02)
        UserCombo(self).setWatchingStatus(show)

    def removeWatchingStatus(self): #can only be run while connected to gateway
        UserCombo(self).removeWatchingStatus()

    def setCustomStatus(self, customstatus, emoji=None, animatedEmoji=False, expires_at=None): #can only be run while connected to gateway
        User(self.RESTurl,self.sessionobj,self.log).setCustomStatusHelper(customstatus, emoji, expires_at, timeout=0.02)
        UserCombo(self).setCustomStatus(customstatus, emoji, animatedEmoji)

    def removeCustomStatus(self):
        User(self.RESTurl,self.sessionobj,self.log).setCustomStatusHelper("", timeout=0.02)
        UserCombo(self).removeCustomStatus()

    def clearActivities(self):
        if self.session.userSettings['custom_status'] != None:
            User(self.RESTurl,self.sessionobj,self.log).setCustomStatusHelper("", emoji=None, expires_at=None, timeout=0.02)
        UserCombo(self).clearActivities()


    '''
    test stuff (these show how to add combo functions)
    '''
    def testfunc(self):
        self.command({'function': GuildCombo(self).testfunc, 'priority': 0})

    def testfuncPOG(self, pog):
        self.command({'function': GuildCombo(self).testfuncPOG, 'priority': 0, 'params': {'pog': pog}})

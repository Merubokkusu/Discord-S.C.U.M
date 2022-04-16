import websocket
import json
import time
import random
import zlib
import copy

try:
	import thread
except ImportError:
	import _thread as thread

#session data, response object, requests, and parsing
from .session import Session
from .response import Resp
from .request import Request
from .parse import Parse

#log to console/file
from ..logger import LogLevel, Logger

#dynamic imports
from ..importmanager import Imports
imports = Imports(
	{
		"User": "discum.user.user",
		"GuildCombo": "discum.gateway.guild.combo",
		"UserCombo": "discum.gateway.user.combo",
	}
)

#exceptions
class InvalidSessionException(Exception):
	pass

class NeedToReconnectException(Exception):
	pass

class ConnectionResumableException(Exception): #for certain close codes. "exception"
	pass

class ConnectionManuallyClosedException(Exception):
	pass

def exceptionChecker(e, types): #this is an A or B or ... check
	for i in types:
		if isinstance(e,i):
			return True
	return False

#gateway class
class GatewayServer:

	__slots__ = ['token', 'super_properties', 'auth', 'RESTurl', 'sessionobj', 'proxy_host', 'proxy_port', 'proxy_type', 'proxy_auth', 'keepData', 'log', 'interval', 'session_id', 'sequence', 'READY', 'session', 'ws', '_after_message_hooks', '_last_err', '_last_close_event', 'connected', 'resumable', 'voice_data', 'memberFetchingStatus', 'resetMembersOnSessionReconnect', 'updateSessionData', 'guildMemberSearches', '_last_ack', 'latency', 'request', 'parse', '_zlib', 'connectionKwargs']

	class OPCODE:
		# Name                         Code  Client Action   Description
		DISPATCH =                     0  #  Receive         dispatches an event
		HEARTBEAT =                    1  #  Send/Receive    used for ping checking
		IDENTIFY =                     2  #  Send            used for client handshake
		PRESENCE_UPDATE =              3  #  Send            used to update the client status
		VOICE_STATE_UPDATE =           4  #  Send            used to join/move/leave voice channels
		VOICE_SERVER_PING =            5  #  Send            used for voice ping checking
		RESUME =                       6  #  Send            used to resume a closed connection
		RECONNECT =                    7  #  Receive         used to tell when to reconnect (sometimes...)
		REQUEST_GUILD_MEMBERS =        8  #  Send            used to request guild members (when searching for members in the search bar of a guild)
		INVALID_SESSION =              9  #  Receive         used to notify client they have an invalid session id
		HELLO =                        10 #  Receive         sent immediately after connecting, contains heartbeat and server debug information
		HEARTBEAT_ACK =                11 #  Sent            immediately following a client heartbeat that was received
		#GUILD_SYNC =                  12 #  Receive         guild_sync but not used anymore
		DM_UPDATE =                    13 #  Send            used to get dm features
		LAZY_REQUEST =                 14 #  Send            discord responds back with GUILD_MEMBER_LIST_UPDATE type SYNC...
		LOBBY_CONNECT =                15 #  ??
		LOBBY_DISCONNECT =             16 #  ??
		LOBBY_VOICE_STATES_UPDATE =    17 #  Receive
		STREAM_CREATE =                18 #  ??
		STREAM_DELETE =                19 #  ??
		STREAM_WATCH =                 20 #  ??
		STREAM_PING =                  21 #  Send
		STREAM_SET_PAUSED =            22 #  ??
		REQUEST_APPLICATION_COMMANDS = 24 #  Send            request application/bot cmds (user, message, and slash cmds)

	def __init__(self, websocketurl, token, super_properties, sessionobj=None, RESTurl="", log={"console":True, "file":False}): #session obj needed for proxies and some combo gateway functions (that also require http api wraps)
		self.token = token
		self.super_properties = super_properties
		self.auth = {
				"token": self.token,
				"capabilities": 509,
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
					"user_guild_settings_version": -1,
					"user_settings_version": -1
				}
			}
		self.RESTurl = RESTurl #for helper http requests
		self.sessionobj = sessionobj #for helper http requests

		self.proxy_type, self.proxy_auth, self.proxy_host, self.proxy_port = [None]*4
		if sessionobj and sessionobj.proxies:
			self.proxy_type = proxy_type = list(sessionobj.proxies.keys())[0]
			self.proxy_host, self.proxy_port = sessionobj.proxies[proxy_type].split('://')[-1].split(':')
			if sessionobj.auth:
				self.proxy_auth = (sessionobj.auth.username, sessionobj.auth.password)

		self.keepData = ("guilds") #keep data even after leaving "dms", "guilds", or "guild_channels"
		self.log = log

		self.interval = None
		self.session_id = None
		self.sequence = 0
		self.READY = False #becomes True once READY_SUPPLEMENTAL is received
		self.session = Session({},{}) #not the same as sessionobj

		#websocket.enableTrace(True) #for debugging
		self.ws = self._get_ws_app(websocketurl)

		self._after_message_hooks = []
		self._last_err = None
		self._last_close_event = None

		self.connected = False
		self.resumable = False

		self.voice_data = {} #voice connections dependent on current (connected) session

		self.memberFetchingStatus = {"first": []}
		self.resetMembersOnSessionReconnect = True #reset members after each session
		self.updateSessionData = True
		self.guildMemberSearches = {}

		#latency
		self._last_ack = None
		self.latency = None

		#gateway requests and parsing
		self.request = Request(self)
		self.parse = Parse

		#extra gateway connection kwargs
		self.connectionKwargs = {}

	#WebSocketApp, more info here: https://github.com/websocket-client/websocket-client/blob/master/websocket/_app.py#L84
	def _get_ws_app(self, websocketurl):
		headers = {
			"Accept-Encoding": "gzip, deflate, br",
			"Accept-Language": "en-US,en;q=0.9",
			"Cache-Control": "no-cache",
			"Pragma": "no-cache",
			"Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
			"User-Agent": self.super_properties["browser_user_agent"]
		} #more info: https://stackoverflow.com/a/40675547

		ws = websocket.WebSocketApp(websocketurl,
									header = headers,
									on_open=lambda ws: self.on_open(ws),
									on_message=lambda ws, msg: self.on_message(ws, msg),
									on_error=lambda ws, msg: self.on_error(ws, msg),
									on_close=lambda ws, close_code, close_msg: self.on_close(ws, close_code, close_msg)
									)
		return ws

	def decompress(self, bmessage): #input is byte message
		data = self._zlib.decompress(bmessage)
		jsonmessage = json.loads(data.decode("UTF8"))
		return jsonmessage

	def on_open(self, ws):
		self.connected = True
		self.memberFetchingStatus = {"first": []}
		Logger.log("[gateway] Connected to websocket.", None, self.log)
		if not self.resumable:
			#send presences if 1 or more activites in previous session. Whether or not you're invisible doesn't matter apparently.
			if len(self.session.settings_ready) != 0:
				if self.session.userSettings.get("activities") not in (None, {}):
					self.auth["presence"]["status"] = self.session.userSettings.get("status")
					self.auth["presence"]["activities"] = imports.UserCombo(self).constructActivitiesList()
			self.send({"op": self.OPCODE.IDENTIFY, "d": self.auth})
			self.send({"op": self.OPCODE.VOICE_STATE_UPDATE, "d": {"guild_id": None, "channel_id": None, "self_mute": True, "self_deaf": False, "self_video": False}})
			
		else:
			self.resumable = False
			self.send({"op": self.OPCODE.RESUME, "d": {"token": self.token, "session_id": self.session_id, "seq": self.sequence-1 if self.sequence>0 else self.sequence}})

	def on_message(self, ws, message):
		response = self.decompress(message)
		if response['op'] != self.OPCODE.HEARTBEAT_ACK:
			self.sequence += 1
		resp = Resp(copy.deepcopy(response))
		Logger.log('[gateway] < {}'.format(response), LogLevel.RECEIVE, self.log)
		if response['op'] == self.OPCODE.HELLO: #only happens once, first message sent to client
			self.interval = (response["d"]["heartbeat_interval"])/1000 #if this fails make an issue and I'll revert it back to the old method (slightly smaller wait time than heartbeat)
			thread.start_new_thread(self._heartbeat, ())
		elif response['op'] == self.OPCODE.HEARTBEAT_ACK:
			if self._last_ack != None:
				self.latency = time.perf_counter() - self._last_ack
		elif response['op'] == self.OPCODE.HEARTBEAT:
			self.send({"op": self.OPCODE.HEARTBEAT,"d": self.sequence})
		elif response['op'] == self.OPCODE.INVALID_SESSION:
			Logger.log("[gateway] Invalid session.", None, self.log)
			self._last_err = InvalidSessionException("Invalid Session Error.")
			if self.resumable:
				self.resumable = False
				self.sequence = 0
				self.close()
			else:
				self.sequence = 0
				self.close()
		elif response['op'] == self.OPCODE.RECONNECT:
			Logger.log("[gateway] Received opcode 7 (reconnect).", None, self.log)
			self._last_err = NeedToReconnectException("Discord sent an opcode 7 (reconnect).")
			self.close()
		if self.interval == None:
			Logger.log("[gateway] Identify failed.", None, self.log)
			self.close()
		if resp.event.ready:
			self._last_err = None
			self.session_id = response['d']['session_id']
			settings_ready = resp.parsed.ready() #parsed
			if not self.resetMembersOnSessionReconnect and self.session.read()[0]:
				for guildID in settings_ready['guilds']:
					settings_ready['guilds'][guildID]['members'] = self.session.guild(guildID).members
			self.session.setSettingsReady(settings_ready)
		elif resp.event.ready_supplemental:
			settings_ready_supp = resp.parsed.ready_supplemental() #parsed
			self.session.setSettingsReadySupp(settings_ready_supp)
			self.READY = True
		if self.updateSessionData:
			self.sessionUpdates(resp)
		thread.start_new_thread(self._response_loop, (resp,))

	def on_error(self, ws, error):
		Logger.log('[gateway] < {}'.format(error), LogLevel.WARNING, self.log)
		self._last_err = error

	def on_close(self, ws, close_code, close_msg):
		self.connected = False
		self.READY = False #reset self.READY
		if close_code or close_msg:
			self._last_close_event = {"code": close_code, "reason": close_msg}
			Logger.log("[gateway] close status code: " + str(close_code), None, self.log)
			Logger.log("[gateway] close message: " + str(close_msg), None, self.log)
			if not (4000<close_code<=4010):
				self.resumable = True
				self._last_err = ConnectionResumableException("Connection is resumable.")
			if close_code in (None, 1000, 1001, 1006):
				self._last_err = ConnectionManuallyClosedException("Disconnection initiated by client using close function.")
		Logger.log('[gateway] websocket closed', None, self.log)

	#Discord needs heartbeats, or else connection will sever
	def _heartbeat(self):
		Logger.log("[gateway] entering heartbeat", None, self.log)
		while self.connected:
			if self.interval == None: #can't replicate the issue so consider this a temp patch
				self.interval = 41.25
			time.sleep(self.interval)
			if not self.connected:
				break
			self.send({"op": self.OPCODE.HEARTBEAT,"d": self.sequence})
			self._last_ack = time.perf_counter()
		return

	#just a wrapper for ws.send
	def send(self, payload):
		Logger.log('[gateway] > {}'.format(payload), LogLevel.SEND, self.log)
		self.ws.send(json.dumps(payload))

	def close(self):
		self.connected = False
		self.READY = False #reset self.READY
		if not exceptionChecker(self._last_err, [InvalidSessionException, NeedToReconnectException]):
			self._last_err = ConnectionManuallyClosedException("Disconnection initiated by client using close function.")
		Logger.log('[gateway] websocket closed', None, self.log) #don't worry if this message prints twice
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
	def _response_loop(self, resp): #thx ToasterUwU for bringing up dummy threads
		commandslist = self._after_message_hooks[:] #create a copy
		for func in commandslist:
			if callable(func):
				func(resp)
			elif isinstance(func, dict):
				function = func['function']
				params = func['params'] if 'params' in func else {}
				function(resp, **params)
		return

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
			Logger.log('{} not found in _after_message_hooks.'.format(func), None, self.log)
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
		self._last_ack = None
		self.memberFetchingStatus = {"first": []}

	#kinda influenced by https://github.com/scrubjay55/Reddit_ChatBot_Python (Apache License 2.0)
	def run(self, auto_reconnect=True):
		if auto_reconnect:
			while True:
				try:
					self._zlib = zlib.decompressobj()
					self.ws.run_forever(
						ping_interval=10,
						ping_timeout=5,
						http_proxy_host=self.proxy_host,
						http_proxy_port=self.proxy_port,
						http_proxy_auth=self.proxy_auth,
						proxy_type=self.proxy_type,
						**self.connectionKwargs
					)
					raise self._last_err
				except KeyboardInterrupt:
					self._last_err = KeyboardInterrupt("Keyboard Interrupt Error")
					Logger.log("[gateway] Connection forcibly closed using Keyboard Interrupt.", None, self.log)
					break
				except Exception as e:
					if auto_reconnect:
						if not exceptionChecker(e, [KeyboardInterrupt]):
							if exceptionChecker(e, [ConnectionResumableException]):
								self._last_err = None
								waitTime = random.randrange(1,6)
								Logger.log("[gateway] Connection Dropped. Attempting to resume last valid session in {} seconds.".format(waitTime), None, self.log)
								time.sleep(waitTime)
							elif exceptionChecker(e, [ConnectionManuallyClosedException]):
								Logger.log("[gateway] Connection forcibly closed using close function.", None, self.log)
								break
							else:
								self.resetSession()
								Logger.log("[gateway] Connection Dropped. Retrying in 10 seconds.", None, self.log)
								time.sleep(10)
		else:
			self._zlib = zlib.decompressobj()
			self.ws.run_forever(
				ping_interval=10,
				ping_timeout=5,
				http_proxy_host=self.proxy_host,
				http_proxy_port=self.proxy_port,
				http_proxy_auth=self.proxy_auth,
				proxy_type=self.proxy_type,
				**self.connectionKwargs
			)

	######################################################
	def sessionUpdates(self, resp):
		#***guilds
		#guild created
		if resp.event.guild:
			guildData = resp.parsed.guild_create(my_user_id=self.session.user['id']) #user id needed for updating personal roles in that guild
			guildID = guildData['id']
			voiceStateData = guildData.pop('voice_states', [])
			if not self.resetMembersOnSessionReconnect and guildID in self.session.guildIDs:
				guildData['members'] = self.session.guild(guildID).members
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
	#op14 related stuff
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
		if guild_id in self.memberFetchingStatus and reset:
			del self.memberFetchingStatus[guild_id] #just resetting tracker on the specific guild_id
		self.command(
			{
				"function": imports.GuildCombo(self).fetchMembers,
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

	def findVisibleChannels(self, guildID, types=['guild_text', 'dm', 'guild_voice', 'group_dm', 'guild_category', 'guild_news', 'guild_store', 'guild_news_thread', 'guild_public_thread', 'guild_private_thread', 'guild_stage_voice'], findFirst=False):
		if len(self.session.read()[0]) == 0: #if never connected to gateway
			return
		return imports.GuildCombo(self).findVisibleChannels(guildID, types, findFirst)

	#sends a series of opcode 14s to tell discord that you're looking at guild channels
	def subscribeToGuildEvents(self, onlyLarge=False, wait=None):
		imports.GuildCombo(self).subscribeToGuildEvents(onlyLarge, wait)

	#op8 related stuff
	def queryGuildMembers(self, guildIDs, query, saveAsQueryOverride=None, limit=10, presences=True, keep=[]):
		if isinstance(guildIDs, str):
			guildIDs = [guildIDs]
		imports.GuildCombo(self).searchGuildMembers(guildIDs, query, saveAsQueryOverride, limit, presences, None, keep)

	def checkGuildMembers(self, guildIDs, userIDs, presences=True, keep=[]):
		if isinstance(guildIDs, str):
			guildIDs = [guildIDs]
		imports.GuildCombo(self).searchGuildMembers(guildIDs, "", None, 10, presences, userIDs, keep)

	def finishedGuildSearch(self, guildIDs, query="", saveAsQueryOverride=None, userIDs=None, keep=False):
		if isinstance(guildIDs, str):
			guildIDs = [guildIDs]
		saveAsQuery = query.lower() if saveAsQueryOverride==None else saveAsQueryOverride.lower()
		command = {
			"function": imports.GuildCombo(self).handleGuildMemberSearches,
			"params": {
				"guildIDs": guildIDs,
				"saveAsQuery": saveAsQuery,
				"isQueryOverridden": saveAsQueryOverride != None,
				"userIDs": userIDs,
				"keep": keep
			},
		}
		if keep == False: #if keep param not provided, look if params are subset of command_list function params
			command["params"].pop("keep")
			for c in self._after_message_hooks:
				if isinstance(c, dict):
					if c.get("function").__func__ == imports.GuildCombo(self).handleGuildMemberSearches.__func__:
						d1 = command["params"]
						d2 = c.get("params", {})
						if all(key in d2 and d2[key] == d1[key] for key in d1): #https://stackoverflow.com/a/41579450/14776493
							return False #not finished yet with guild search
			return True
		else:
			return command not in self._after_message_hooks

	'''
	User stuff
	'''
	def setStatus(self, status): #can only be run while connected to gateway
		imports.User(self.RESTurl,self.sessionobj,self.log).setStatusHelper(status)
		imports.UserCombo(self).setStatus(status)

	def setPlayingStatus(self, game): #can only be run while connected to gateway, will update metadata later
		if not self.session.userSettings['show_current_game']:
			imports.User(self.RESTurl,self.sessionobj,self.log).enableActivityDisplay(enable=True)
		imports.UserCombo(self).setPlayingStatus(game)

	def removePlayingStatus(self): #can only be run while connected to gateway
		imports.UserCombo(self).removePlayingStatus()

	def setStreamingStatus(self, stream, url): #can only be run while connected to gateway, will update metadata later
		if not self.session.userSettings['show_current_game']:
			imports.User(self.RESTurl,self.sessionobj,self.log).enableActivityDisplay(enable=True)
		imports.UserCombo(self).setStreamingStatus(stream, url)

	def removeStreamingStatus(self): #can only be run while connected to gateway
		imports.UserCombo(self).removeStreamingStatus()

	def setListeningStatus(self, song): #can only be run while connected to gateway, will update metadata later
		if not self.session.userSettings['show_current_game']:
			imports.User(self.RESTurl,self.sessionobj,self.log).enableActivityDisplay(enable=True)
		imports.UserCombo(self).setListeningStatus(song)

	def removeListeningStatus(self): #can only be run while connected to gateway
		imports.UserCombo(self).removeListeningStatus()

	def setWatchingStatus(self, show): #can only be run while connected to gateway, will update metadata later
		if not self.session.userSettings['show_current_game']:
			imports.User(self.RESTurl,self.sessionobj,self.log).enableActivityDisplay(enable=True)
		imports.UserCombo(self).setWatchingStatus(show)

	def removeWatchingStatus(self): #can only be run while connected to gateway
		imports.UserCombo(self).removeWatchingStatus()

	def setCustomStatus(self, customstatus, emoji=None, animatedEmoji=False, expires_at=None): #can only be run while connected to gateway
		imports.User(self.RESTurl,self.sessionobj,self.log).setStatusHelper(self.session.userSettings['status'])
		imports.User(self.RESTurl,self.sessionobj,self.log).setCustomStatusHelper(customstatus, emoji, expires_at)
		imports.UserCombo(self).setCustomStatus(customstatus, emoji, animatedEmoji)

	def removeCustomStatus(self):
		imports.User(self.RESTurl,self.sessionobj,self.log).setCustomStatusHelper("")
		imports.UserCombo(self).removeCustomStatus()

	def clearActivities(self):
		if self.session.userSettings['custom_status'] != None:
			imports.User(self.RESTurl,self.sessionobj,self.log).setCustomStatusHelper("", emoji=None, expires_at=None)
		imports.UserCombo(self).clearActivities()

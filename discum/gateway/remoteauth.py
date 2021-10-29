'''
sources used:
https://luna.gitlab.io/discord-unofficial-docs/desktop_remote_auth.html
https://github.com/Vap0r1ze/discord-remote-auth/blob/master/src/types/RemoteAuthClient.js
'''
import websocket
import time

import json
import base64

try:
	from Crypto.PublicKey import RSA
	from Crypto.Cipher import PKCS1_OAEP
	from Crypto.Hash import SHA256
	import pyqrcode
except ImportError:
	raise ImportError("Install discum[ra] to use remote authentication.")

try:
	import thread
except ImportError:
	import _thread as thread

from ..logger import *

class RemoteAuth:

	__slots__ = ['user_agent', 'saveQrCode', 'proxy_host', 'proxy_port', 'log', '_last_err', '_after_message_hooks', 'connected', 'interval', 'key_pair', 'public_key', 'decryptor', 'fingerprint', 'qr_url', 'qr_img', 'userData', 'token', 'ws']

	class OPCODE:
		# Name                 Code                      Client Action   Description
		HELLO =                "hello"  #                Receive         sent on connection open
		INIT =                 "init"  #                 Send            describes generated public key
		NONCE_PROOF =          "nonce_proof"  #          Send/Receive    encrypted nonce from server, decrypted nonce from client as "proof"
		PENDING_REMOTE_INIT =  "pending_remote_init"  #  Receive         sent after a valid nonce_proof is submitted
		PENDING_FINISH =       "pending_finish"  #       Receive         sent after QR code is scanned, contains encrypted user data
		FINISH =               "finish"  #               Receive         sent after login flow is completed, contains encrypted token
		CANCEL =               "cancel"  #               Receive         cancel qr code login
		HEARTBEAT =            "heartbeat"  #            Send            sent every N ms, described in hello packet
		HEARTBEAT_ACK =        "heartbeat_ack"  #        Receive         sent after heartbeat packet, should close connection if a heartbeat_ack isn't received by the next heartbeat interval

	def __init__(self, remoteauthurl, user_agent, proxy_host=None, proxy_port=None, log={"console":True, "file":False}):
		self.user_agent = user_agent
		self.saveQrCode = True
		self.proxy_host = proxy_host
		self.proxy_port = proxy_port
		self.log = log
		self._last_err = None
		self._after_message_hooks = []
		self.connected = False
		self.interval = None
		self.key_pair = None
		self.public_key = None
		self.decryptor = None
		self.fingerprint = None
		self.qr_url = None
		self.qr_img = None
		self.userData = None
		self.token = None
		self.ws = self._get_ws_app(remoteauthurl)

	#WebSocketApp, more info here: https://github.com/websocket-client/websocket-client/blob/master/websocket/_app.py#L84
	def _get_ws_app(self, remoteauthurl):
		headers = {
			"Accept-Encoding": "gzip, deflate, br",
			"Accept-Language": "en-US,en;q=0.9",
			"Cache-Control": "no-cache",
			"Pragma": "no-cache",
			"Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
			"User-Agent": self.user_agent
		} #more info: https://stackoverflow.com/a/40675547

		ws = websocket.WebSocketApp(remoteauthurl,
									header = headers,
									on_open=lambda ws: self.on_open(ws),
									on_message=lambda ws, msg: self.on_message(ws, msg),
									on_error=lambda ws, msg: self.on_error(ws, msg),
									on_close=lambda ws, close_code, close_msg: self.on_close(ws, close_code, close_msg)
									)
		return ws

	def decrypt(self, data):
		decoded = base64.b64decode(data)
		decrypted = self.decryptor.decrypt(decoded)
		return decrypted

	def parseUserPayload(self, data):
		user_data = data.decode('utf-8').split(':')
		userID = user_data[0]
		username = user_data[3]
		discriminator = user_data[1]
		avatarName = user_data[2]
		if avatarName == '0':
			avatar = 'https://cdn.discordapp.com/embed/avatars/{}.png'.format(int(discriminator) % 5)
		elif avatarName.startwith('a_'):
			avatar = 'https://cdn.discordapp.com/avatars/{}/{}.gif'.format(userID, avatarName)
		else:
			avatar = 'https://cdn.discordapp.com/avatars/{}/{}.png'.format(userID, avatarName)
		return userID, username, discriminator, avatar

	def on_open(self, ws):
		self.connected = True
		Logger.log("[ra] Connected to websocket.", None, self.log)

	def on_message(self, ws, message):
		response = json.loads(message)
		Logger.log('[ra] < {}'.format(response), LogLevel.RECEIVE, self.log)
		op = response['op']
		if op == self.OPCODE.HELLO:
			self.interval = (response["heartbeat_interval"])/1000
			thread.start_new_thread(self._heartbeat, ())
			cert = self.public_key.exportKey()
			encoded_public_key = cert.decode('utf-8').replace('\n','')[26:-24]
			self.send({"op":self.OPCODE.INIT, "encoded_public_key":encoded_public_key})
		elif op == self.OPCODE.NONCE_PROOF:
			nonce = self.decrypt(response['encrypted_nonce'])
			digest = SHA256.new(nonce).digest()
			nonce_proof = base64.urlsafe_b64encode(digest).decode('utf-8').rstrip('=')
			self.send({"op": self.OPCODE.NONCE_PROOF, "proof": nonce_proof})
		elif op == self.OPCODE.PENDING_REMOTE_INIT:
			self.fingerprint = response['fingerprint']
			self.qr_url = 'https://discordapp.com/ra/{}'.format(self.fingerprint)
			self.qr_img = pyqrcode.create(self.qr_url, error='H')
			if self.saveQrCode: #self.qr_img.show() wasn't working consistently
				if isinstance(self.saveQrCode, str):
					fileLoc = self.saveQrCode
				else:
					fileLoc = self.fingerprint+".png"
				self.qr_img.png(fileLoc, scale=10)
				print("QR code image for {} saved in {}".format(self.fingerprint, fileLoc))
		elif op == self.OPCODE.PENDING_FINISH:
			user_payload = self.decrypt(response['encrypted_user_payload'])
			userID, username, discriminator, avatar = self.parseUserPayload(user_payload)
			self.userData = {
				'id': userID,
				'username': username,
				'discriminator': discriminator,
				'avatar': avatar
			}
		elif response['op'] == self.OPCODE.FINISH:
			self.token = self.decrypt(response['encrypted_token']).decode('utf-8')
		if self.interval == None:
			Logger.log("[ra] Connection failed.", None, self.log)
			self.close()
		thread.start_new_thread(self._response_loop, (response,))

	def on_error(self, ws, error):
		Logger.log('[ra] < {}'.format(error), LogLevel.WARNING, self.log)
		self._last_err = error

	def on_close(self, ws, close_code, close_msg):
		self.connected = False
		if close_code or close_msg:
			self._last_close_event = {"code": close_code, "reason": close_msg}
			print(self._last_close_event)
		Logger.log('[ra] websocket closed', None, self.log)

	def _heartbeat(self):
		Logger.log("[ra] entering heartbeat", None, self.log)
		while self.connected:
			time.sleep(self.interval)
			if not self.connected:
				break
			self.send({"op": self.OPCODE.HEARTBEAT})
		return

	#just a wrapper for ws.send
	def send(self, payload):
		Logger.log('[ra] > {}'.format(payload), LogLevel.SEND, self.log)
		self.ws.send(json.dumps(payload))

	def close(self):
		self.connected = False
		Logger.log('[ra] websocket closed', None, self.log)
		self.ws.close()

	def command(self, func):
		if callable(func):
			self._after_message_hooks.append(func)
			return func
		elif isinstance(func, dict):
			priority = func.pop('priority', len(self._after_message_hooks))
			self._after_message_hooks.insert(priority, func)
			return func['function']

	#kinda influenced by https://github.com/scrubjay55/Reddit_ChatBot_Python (Apache License 2.0)
	def _response_loop(self, response):
		commandslist = self._after_message_hooks[:] #create a copy
		for func in commandslist:
			if callable(func):
				func(response)
			elif isinstance(func, dict):
				function = func['function']
				params = func['params'] if 'params' in func else {}
				function(response, **params)
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

	def resetSession(self):
		self._last_err = None
		self.connected = False
		self.interval = None
		self.key_pair = RSA.generate(2048)
		self.public_key = self.key_pair.publickey()
		self.decryptor = PKCS1_OAEP.new(self.key_pair, SHA256)
		self.fingerprint = None
		self.qr_url = None
		self.qr_img = None
		self.userData = None
		self.token = None

	def run(self, saveQrCode=True):
		self.saveQrCode = saveQrCode
		self.resetSession()
		self.ws.run_forever(ping_interval=10, ping_timeout=5, http_proxy_host=self.proxy_host, http_proxy_port=self.proxy_port)
		return self.token, self.userData
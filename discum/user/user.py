import base64
from ..RESTapiwrap import *

class User(object):
	def __init__(self, discord, s, log): #s is the requests session object
		self.discord = discord
		self.s = s
		self.log = log
		
	#def getDMs(self): #websockets does this now
	#	url = self.discord+"users/@me/channels"
	#	return self.s.get(url)

	#def getGuilds(self): #websockets does this now
	#	url = self.discord+"users/@me/guilds"
	#	return self.s.get(url)

	#def getRelationships(self): #websockets does this now
	#	url = self.discord+"users/@me/relationships"
	#	return self.s.get(url)

	def requestFriend(self,user):
		if "#" in user:
			url = self.discord+"users/@me/relationships"
			body = {"username": user.split("#")[0], "discriminator": int(user.split("#")[1])}
			return Wrapper.sendRequest(self.s, 'post', url, body, log=self.log)
		else:
			url = self.discord+"users/@me/relationships/"+user
			body = {}
			return Wrapper.sendRequest(self.s, 'put', url, body, log=self.log)

	def acceptFriend(self,userID):
		url = self.discord+"users/@me/relationships/"+userID
		body = {}
		return Wrapper.sendRequest(self.s, 'put', url, body, log=self.log)

	def removeRelationship(self,userID): #for removing friends, unblocking people
		url = self.discord+"users/@me/relationships/"+userID
		return Wrapper.sendRequest(self.s, 'delete', url, log=self.log)

	def blockUser(self,userID):
		url = self.discord+"users/@me/relationships/"+userID
		body = {"type": 2}
		return Wrapper.sendRequest(self.s, 'put', url, body, log=self.log)

	def getProfile(self,userID):
		url = self.discord+"users/"+userID+"/profile"
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	def info(self, with_analytics_token=None): #simple. bot.info() for own user data
		url = self.discord+"users/@me"
		if with_analytics_token!=None:
			with_analytics_token = str(with_analytics_token).lower()
			url += "?with_analytics_token="+with_analytics_token
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	def getUserAffinities(self):
		url = self.discord+"users/@me/affinities/users"
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	#guild affinities with respect to current user, decided to organize this wrap in here b/c that's how the api is organized
	def getGuildAffinities(self):
		url = self.discord+"users/@me/affinities/guilds"
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	def getMentions(self, limit=25, roleMentions=True, everyoneMentions=True):
		roleMentions = str(roleMentions).lower()
		everyoneMentions = str(everyoneMentions).lower()
		url = self.discord+"users/@me/mentions?limit="+str(limit)+"&roles="+roleMentions+"&everyone="+everyoneMentions
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	def removeMentionFromInbox(self, messageID):
		url = self.discord+"users/@me/mentions/"+messageID
		return Wrapper.sendRequest(self.s, 'delete', url, log=self.log)

	def getMyStickers(self):
		url = self.discord+"users/@me/sticker-packs"
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	'''
	Profile Edits
	'''	
	def setStatus(self,status): #status options are: online, idle, dnd, invisible
		url = self.discord+"users/@me/settings"
		if status in ("online", "idle", "dnd", "invisible"):
			body = {"status": status}
		elif status in ('', None):
			body = {"custom_status": None}
		else:
			body = {"custom_status":{"text": str(status)}}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def setAvatar(self, imagePath): #local image
		url = self.discord+"users/@me"
		with open(imagePath, "rb") as image:
			encodedImage = base64.b64encode(image.read()).decode('utf-8')
		body = {"avatar":"data:image/png;base64,"+encodedImage}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def setUsername(self, username, password):
		url = self.discord+"users/@me"
		body = {"username": username, "password": password}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def setEmail(self, email, password):
		url = self.discord+"users/@me"
		body = {"email": email, "password": password}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def setPassword(self, new_password, password):
		url = self.discord+"users/@me"
		body = {"password": password, "new_password": new_password}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def setDiscriminator(self, discriminator, password):
		url = self.discord+"users/@me"
		body = {"password":password, "discriminator":discriminator}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)
	'''
	More settings stuff
	'''
	def setHypesquad(self, house):
		url = self.discord+"hypesquad/online"
		if house.lower() == "bravery":
			body = {"house_id": 1}
		elif house.lower() == "brilliance":
			body = {"house_id": 2}
		elif house.lower() == "balance":
			body = {"house_id": 3}
		return Wrapper.sendRequest(self.s, 'post', url, body, log=self.log)

	def leaveHypesquad(self):
		url = self.discord+"hypesquad/online"
		return Wrapper.sendRequest(self.s, 'delete', url, log=self.log)

	def setLocale(self, locale):
		url = self.discord+"users/@me/settings"
		body = {"locale": locale}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def enable2FA(self, code, secret, password): #returns new token plus backup codes
		url = self.discord+"users/@me/mfa/totp/enable"
		body = {"code": code, "secret": secret, "password": password}
		return Wrapper.sendRequest(self.s, 'post', url, body, log=self.log)

	def disable2FA(self, code):
		url = self.discord+"users/@me/mfa/totp/disable"
		body = {"code": code}
		return Wrapper.sendRequest(self.s, 'post', url, body, log=self.log)

	def getRTCregions(self):
		url = "https://latency.discord.media/rtc"
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	def setAFKtimeout(self, timeout_seconds):
		url = self.discord+"users/@me/settings"
		body = {"afk_timeout": timeout_seconds}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def setTheme(self, theme):
		url = self.discord+"users/@me/settings"
		body = {"theme": theme.lower()}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def setMessageDisplay(self, CozyOrCompact):
		url = self.discord+"users/@me/settings"
		if CozyOrCompact.lower() == "compact":
			body = {"message_display_compact": True}
		else:
			body = {"message_display_compact": False}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def enableDevMode(self, enable):
		url = self.discord+"users/@me/settings"
		body = {"developer_mode": enable}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def activateApplicationTestMode(self, applicationID):
		url = self.discord+"applications/"+applicationID+"/skus"
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	def getApplicationData(self, applicationID, with_guild=False):
		url = self.discord+"applications/"+applicationID+"/public?with_guild="+str(with_guild).lower()
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	def getBackupCodes(self, password, regenerate=False):
		url = self.discord+"users/@me/mfa/codes"
		body = {"password": password, "regenerate": regenerate}
		return Wrapper.sendRequest(self.s, 'post', url, body, log=self.log)

	'''
	App Settings - Text&Images
	'''
	def enableInlineMedia(self, enable):
		url = self.discord+"users/@me/settings"
		body = {"inline_embed_media": enable}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def enableLargeImagePreview(self, enable):
		url = self.discord+"users/@me/settings"
		body = {"inline_attachment_media": enable}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def enableGifAutoPlay(self, enable):
		url = self.discord+"users/@me/settings"
		body = {"gif_auto_play": enable}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def enableLinkPreview(self, enable):
		url = self.discord+"users/@me/settings"
		body = {"render_embeds": enable}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def enableReactionRendering(self, enable):
		url = self.discord+"users/@me/settings"
		body = {"render_reactions": enable}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def enableAnimatedEmoji(self, enable):
		url = self.discord+"users/@me/settings"
		body = {"animate_emoji": enable}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def enableEmoticonConversion(self, enable):
		url = self.discord+"users/@me/settings"
		body = {"convert_emoticons": enable}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def stickerAnimation(self, setting):
		url = self.discord+"users/@me/settings"
		if setting.lower() == "always":
			body = {"animate_stickers": 0}
		elif setting.lower() == "interaction":
			body = {"animate_stickers": 1}
		elif setting.lower() == "never":
			body = {"animate_stickers": 2}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def enableTTS(self, enable):
		url = self.discord+"users/@me/settings"
		body = {"enable_tts_command": enable}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	'''
	Billing Settings - Billing
	'''
	def getBillingHistory(self, limit=20):
		url = self.discord+"users/@me/billing/payments?limit="+str(limit)
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	def getPaymentSources(self):
		url = self.discord+"users/@me/billing/payment-sources"
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	def getBillingSubscriptions(self):
		url = self.discord+"users/@me/billing/subscriptions"
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	def getStripeClientSecret(self): #for adding new payment methods. Stripe api wraps are not included because discum is just a discord api wrapper.
		url = self.discord+"users/@me/billing/stripe/setup-intents"
		return Wrapper.sendRequest(self.s, 'post', url, log=self.log)
	'''
	Billing Settings - Gift Inventory
	'''
	
	'''
	Logout
	'''
	def logout(self, provider=None, voip_provider=None):
		url = self.discord+"auth/logout"
		body = {"provider": provider, "voip_provider": voip_provider}
		return Wrapper.sendRequest(self.s, 'post', url, body, log=self.log)


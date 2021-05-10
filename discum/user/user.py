import base64
import datetime
from ..RESTapiwrap import *

class User(object):
	def __init__(self, discord, s, log): #s is the requests session object
		self.discord = discord
		self.s = s
		self.log = log

	def requestFriend(self, user):
		if "#" in user:
			url = self.discord+"users/@me/relationships"
			body = {"username": user.split("#")[0], "discriminator": int(user.split("#")[1])}
			return Wrapper.sendRequest(self.s, 'post', url, body, log=self.log)
		else:
			url = self.discord+"users/@me/relationships/"+user
			body = {}
			return Wrapper.sendRequest(self.s, 'put', url, body, log=self.log)

	def acceptFriend(self, userID):
		url = self.discord+"users/@me/relationships/"+userID
		body = {}
		return Wrapper.sendRequest(self.s, 'put', url, body, log=self.log)

	def removeRelationship(self, userID): #for removing friends, unblocking people
		url = self.discord+"users/@me/relationships/"+userID
		return Wrapper.sendRequest(self.s, 'delete', url, log=self.log)

	def blockUser(self, userID):
		url = self.discord+"users/@me/relationships/"+userID
		body = {"type": 2}
		return Wrapper.sendRequest(self.s, 'put', url, body, log=self.log)

	def getProfile(self, userID):
		url = self.discord+"users/"+userID+"/profile"
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	def info(self, with_analytics_token): #simple. bot.info() for own user data
		url = self.discord+"users/@me"
		if with_analytics_token:
			with_analytics_token = str(with_analytics_token).lower()
			url += "?with_analytics_token="+with_analytics_token
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	def getConnectedAccounts(self):
		url = self.discord+"users/@me/connections"
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	def getUserAffinities(self):
		url = self.discord+"users/@me/affinities/users"
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	#guild affinities with respect to current user, decided to organize this wrap in here b/c that's how the api is organized
	def getGuildAffinities(self):
		url = self.discord+"users/@me/affinities/guilds"
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	def getMentions(self, limit, roleMentions, everyoneMentions):
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

	def getNotes(self, userID):
		url = self.discord+"users/@me/notes/"+userID
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	def setStatusHelper(self, status, timeout=None): #Dont run this function by itself; status options are: online, idle, dnd, invisible
		url = self.discord+"users/@me/settings"
		if status in ("online", "idle", "dnd", "invisible"):
			body = {"status": status}
		return Wrapper.sendRequest(self.s, 'patch', url, body, timeout=timeout, log=self.log)

	def setCustomStatusHelper(self, customstatus, emoji, expires_at, timeout=None): #Dont run this function by itself
		url = self.discord+"users/@me/settings"
		body = {"custom_status": {}}
		if customstatus not in (None, ""):
			body["custom_status"]["text"] = customstatus
		if emoji != None:
			if ":" in emoji:
				name, ID = emoji.split(":")
				body["custom_status"]["emoji_name"] = name
				body["custom_status"]["emoji_id"] = ID
			else:
				body["custom_status"]["emoji_name"] = emoji
		if expires_at != None: #assume unix timestamp
			expires_at = float(expires_at)
			dt = datetime.datetime.fromtimestamp(expires_at)
			timestamp = dt.isoformat("T")+"Z"
			body["custom_status"]["expires_at"] = timestamp
		if body["custom_status"] == {}:
			body["custom_status"] = None
		return Wrapper.sendRequest(self.s, 'patch', url, body, timeout=timeout, log=self.log)

	# USER SETTINGS
	'''
	My Account
	'''	
	def setAvatar(self, imagePath): #local image, set to None to delete avatar
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

	def enable2FA(self, code, secret, password): #returns new token plus backup codes
		url = self.discord+"users/@me/mfa/totp/enable"
		body = {"code": code, "secret": secret, "password": password}
		return Wrapper.sendRequest(self.s, 'post', url, body, log=self.log)

	def disable2FA(self, code):
		url = self.discord+"users/@me/mfa/totp/disable"
		body = {"code": code}
		return Wrapper.sendRequest(self.s, 'post', url, body, log=self.log)

	def getBackupCodes(self, password, regenerate):
		url = self.discord+"users/@me/mfa/codes"
		body = {"password": password, "regenerate": regenerate}
		return Wrapper.sendRequest(self.s, 'post', url, body, log=self.log)

	def disableAccount(self, password):
		url = self.discord+"users/@me/disable"
		body = {"password": password}
		return Wrapper.sendRequest(self.s, 'post', url, body, log=self.log)

	def deleteAccount(self, password):
		url = self.discord+"users/@me/delete"
		body = {"password": password}
		return Wrapper.sendRequest(self.s, 'post', url, body, log=self.log)

	'''
	Privacy & Safety
	'''
	def setDMscanLvl(self, level):
		url = self.discord+"users/@me/settings"
		body = {"explicit_content_filter": int(level)}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def allowDMsFromServerMembers(self, allow, disallowedGuildIDs):
		url = self.discord+"users/@me/settings"
		body = {"restricted_guilds":disallowedGuildIDs, "default_guilds_restricted":not allow}
		if not disallowedGuildIDs: #if False or None
			body.pop("restricted_guilds")
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def allowFriendRequestsFrom(self, types):
		url = self.discord+"users/@me/settings"
		body = {"friend_source_flags": {"all": True, "mutual_friends": True, "mutual_guilds": True}}
		types = [i.lower().strip() for i in types]
		if "everyone" not in types:
			body["friend_source_flags"]["all"] = False
		if "mutual_friends" not in types:
			body["friend_source_flags"]["mutual_friends"] = False
		if "mutual_guilds" not in types:
			body["friend_source_flags"]["mutual_guilds"] = False
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def analyticsConsent(self, grant, revoke): #personalization, usage_statistics
		url = self.discord+"users/@me/consent"
		body = {"grant":grant,"revoke":revoke}
		return Wrapper.sendRequest(self.s, 'post', url, body, log=self.log)


	################

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

	def getApplicationData(self, applicationID, with_guild):
		url = self.discord+"applications/"+applicationID+"/public?with_guild="+str(with_guild).lower()
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

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

	def setStickerAnimation(self, setting):
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
	def getBillingHistory(self, limit):
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
	Game Activity
	'''
	def enableActivityDisplay(self, enable, timeout=None):
		url = self.discord+"users/@me/settings"
		body = {"show_current_game": enable}
		Wrapper.sendRequest(self.s, 'patch', url, body, timeout=timeout, log=self.log)
	'''
	Logout
	'''
	def logout(self, provider, voip_provider):
		url = self.discord+"auth/logout"
		body = {"provider": provider, "voip_provider": voip_provider}
		return Wrapper.sendRequest(self.s, 'post', url, body, log=self.log)


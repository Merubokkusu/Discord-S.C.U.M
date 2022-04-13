import base64
import datetime

from ..RESTapiwrap import Wrapper
from ..utils.contextproperties import ContextProperties
from ..utils.color import Color
from ..utils.nonce import calculateNonce

class User(object):
	__slots__ = ['discord', 's', 'log']
	def __init__(self, discord, s, log): #s is the requests session object
		self.discord = discord
		self.s = s
		self.log = log

	def getRelationships(self):
		url = self.discord+"users/@me/relationships"
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	def getMutualFriends(self, userID):
		url = self.discord+"users/"+userID+"/relationships"
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	def requestFriend(self, user):
		if "#" in user:
			url = self.discord+"users/@me/relationships"
			body = {"username": user.split("#")[0], "discriminator": int(user.split("#")[1])}
			return Wrapper.sendRequest(self.s, 'post', url, body, headerModifications={"update":{"X-Context-Properties": ContextProperties.get("add friend")}}, log=self.log)
		else:
			url = self.discord+"users/@me/relationships/"+user
			body = {}
			return Wrapper.sendRequest(self.s, 'put', url, body, headerModifications={"update":{"X-Context-Properties":ContextProperties.get("context menu")}}, log=self.log)

	def acceptFriend(self, userID, location):
		url = self.discord+"users/@me/relationships/"+userID
		body = {}
		return Wrapper.sendRequest(self.s, 'put', url, body, headerModifications={"update":{"X-Context-Properties":ContextProperties.get(location)}}, log=self.log)

	def removeRelationship(self, userID, location): #for removing friends, unblocking people
		url = self.discord+"users/@me/relationships/"+userID
		return Wrapper.sendRequest(self.s, 'delete', url, headerModifications={"update":{"X-Context-Properties":ContextProperties.get(location)}}, log=self.log)

	def blockUser(self, userID, location):
		url = self.discord+"users/@me/relationships/"+userID
		body = {"type": 2}
		return Wrapper.sendRequest(self.s, 'put', url, body, headerModifications={"update":{"X-Context-Properties":ContextProperties.get(location)}}, log=self.log)

	def getProfile(self, userID, with_mutual_guilds, guildID):
		url = self.discord+"users/"+userID+"/profile"
		queries = []
		if with_mutual_guilds != None:
			queries.append("with_mutual_guilds="+repr(with_mutual_guilds).lower())
		if guildID != None:
			queries.append("guild_id="+str(guildID))
		if queries:
			url += '?'+'&'.join(queries)
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	def info(self, with_analytics_token): #simple. bot.info() for own user data
		url = self.discord+"users/@me"
		if with_analytics_token != None:
			url += "?with_analytics_token="+repr(with_analytics_token).lower()
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

	def setUserNote(self, userID, note):
		url = self.discord+'users/@me/notes/'+userID
		body = {"note": note}
		return Wrapper.sendRequest(self.s, 'put', url, body, log=self.log)

	def getRTCregions(self):
		url = "https://latency.discord.media/rtc"
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	def getVoiceRegions(self):
		url = self.discord+'voice/regions'
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
		data = imagePath.split('.')
		imageExt = data[-1] if data[-1] in ('png', 'gif') else 'jpeg'
		body = {"avatar":"data:image/"+imageExt+";base64,"+encodedImage}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def setProfileColor(self, color):
		url = self.discord+"users/@me"
		body = {"accent_color": Color.get(color)}
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

	#as of right now, you need to be in the beta program for this to work
	def setAboutMe(self, bio):
		url = self.discord+"users/@me"
		body = {"bio": bio}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	#as of right now, you need to be in the beta program for this to work
	def setBanner(self, imagePath):
		url = self.discord+"users/@me"
		with open(imagePath, "rb") as image:
			encodedImage = base64.b64encode(image.read()).decode('utf-8')
		body = {"banner":"data:image/png;base64,"+encodedImage}
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

	def setPhone(self, number, reason):
		url = self.discord+"users/@me/phone"
		body = {"phone": number, "change_phone_reason": reason}
		return Wrapper.sendRequest(self.s, 'post', url, body, log=self.log)

	def validatePhone(self, number, code, password):
		url = self.discord+"phone-verifications/verify"
		body = {"phone": number,"code": str(code)}
		request = Wrapper.sendRequest(self.s, 'post', url, body, log=self.log)

		url = self.discord+"users/@me/phone"
		body = {"phone_token":request.json()["token"], "password":password}
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

	def allowScreenReaderTracking(self, allow): #more discord tracking stuff
		url = self.discord+"users/@me/settings"
		body = {"allow_accessibility_detection": allow}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def requestMyData(self):
		url = self.discord+"users/@me/harvest"
		return Wrapper.sendRequest(self.s, 'post', url, log=self.log)

	'''
	Connections
	'''
	def getConnectedAccounts(self):
		url = self.discord+"users/@me/connections"
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	def getConnectionUrl(self, accountType):
		url = self.discord+"connections/"+accountType+"/authorize"
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	def enableConnectionDisplayOnProfile(self, accountType, accountUsername, enable):
		url = self.discord+"users/@me/connections/"+accountType+"/"+accountUsername
		body = {"visibility": enable}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def enableConnectionDisplayOnStatus(self, accountType, accountUsername, enable):
		url = self.discord+"users/@me/connections/"+accountType+"/"+accountUsername
		body = {"show_activity": enable}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def removeConnection(self, accountType, accountUsername):
		url = self.discord+"users/@me/connections/"+accountType+"/"+accountUsername
		return Wrapper.sendRequest(self.s, 'delete', url, log=self.log)

	# BILLING SETTINGS
	'''
	Billing
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

	def getStripeClientSecret(self): #for adding new payment methods. Stripe api wraps are not included because discum is just a discord api 
		url = self.discord+"users/@me/billing/stripe/setup-intents"
		return Wrapper.sendRequest(self.s, 'post', url, log=self.log)

	# APP SETTINGS
	'''
	Appearance
	'''
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

	'''
	Accessibility
	'''
	def enableGifAutoPlay(self, enable):
		url = self.discord+"users/@me/settings"
		body = {"gif_auto_play": enable}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def enableAnimatedEmoji(self, enable):
		url = self.discord+"users/@me/settings"
		body = {"animate_emoji": enable}
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
	Text & Images
	'''

	def enableLinkedImageDisplay(self, enable):
		url = self.discord+"users/@me/settings"
		body = {"inline_embed_media": enable}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def enableImageDisplay(self, enable):
		url = self.discord+"users/@me/settings"
		body = {"inline_attachment_media": enable}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def enableLinkPreview(self, enable):
		url = self.discord+"users/@me/settings"
		body = {"render_embeds": enable}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def enableReactionRendering(self, enable):
		url = self.discord+"users/@me/settings"
		body = {"render_reactions": enable}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def enableEmoticonConversion(self, enable):
		url = self.discord+"users/@me/settings"
		body = {"convert_emoticons": enable}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	'''
	Notifications
	'''
	def setAFKtimeout(self, timeout_seconds):
		url = self.discord+"users/@me/settings"
		body = {"afk_timeout": timeout_seconds}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	'''
	Language
	'''
	def setLocale(self, locale):
		url = self.discord+"users/@me/settings"
		body = {"locale": locale}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	'''
	Advanced
	'''
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

	# ACTIVITY SETTINGS
	'''
	Activity Status
	'''
	def enableActivityDisplay(self, enable, timeout=None):
		url = self.discord+"users/@me/settings"
		body = {"show_current_game": enable}
		Wrapper.sendRequest(self.s, 'patch', url, body, timeout=timeout, log=self.log)

	# OTHER SETTINGS
	'''
	HypeSquad
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

	'''
	Developer Options
	'''
	def getBuildOverrides(self):
		url = "https://discord.com/__development/build_overrides"
		return Wrapper.sendRequest(self.s, 'get', url, headerModifications={"remove":["Authorization", "X-Super-Properties", "X-Fingerprint"]}, log=self.log)

	def enableSourceMaps(self, enable):
		url = "https://discord.com/__development/source_maps"
		if enable:
			return Wrapper.sendRequest(self.s, 'put', url, headerModifications={"remove":["X-Super-Properties", "X-Fingerprint"]}, log=self.log)
		else:
			return Wrapper.sendRequest(self.s, 'delete', url, headerModifications={"remove":["X-Super-Properties", "X-Fingerprint"]}, log=self.log)

	'''
	Notification Settings
	'''
	@staticmethod
	def index(inputList, searchItem): #only used for notification settings, returning -1 doesn't make sense in this context
		try:
			return inputList.index(searchItem)
		except ValueError:
			return 0

	def suppressEveryonePings(self, guildID, suppress):
		url = self.discord+"users/@me/guilds/"+str(guildID)+"/settings"
		body = {"suppress_everyone": suppress}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def suppressRoleMentions(self, guildID, suppress):
		url = self.discord+"users/@me/guilds/"+str(guildID)+"/settings"
		body = {"suppress_roles": suppress}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def enableMobilePushNotifications(self, guildID, enable):
		url = self.discord+"users/@me/guilds/"+str(guildID)+"/settings"
		body = {"mobile_push": enable}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def setChannelNotificationOverrides(self, guildID, overrides):
		url = self.discord+"users/@me/guilds/"+str(guildID)+"/settings"
		if type(overrides[0]) in (tuple, list):
			msgNotificationTypes = ["all messages", "only mentions", "nothing"]
			overrides = {str(channel):{"message_notifications": self.index(msgNotificationTypes, msg.lower()), "muted":muted} for channel,msg,muted in overrides}
		body = {"channel_overrides": overrides}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def setMessageNotifications(self, guildID, notifications):
		url = self.discord+"users/@me/guilds/"+str(guildID)+"/settings"
		msgNotificationTypes = ["all messages", "only mentions", "nothing"]
		body = {"message_notifications": self.index(msgNotificationTypes, notifications.lower())}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def muteGuild(self, guildID, mute, duration):
		url = self.discord+"users/@me/guilds/"+str(guildID)+"/settings"
		body = {"muted": mute}
		if mute and duration is not None:
			end_time = (datetime.datetime.utcnow()+datetime.timedelta(minutes=duration)).isoformat()[:-3]+'Z' #https://stackoverflow.com/a/54272238/14776493
			body["mute_config"] = {"selected_time_window":duration, "end_time":end_time}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def muteDM(self, DMID, mute, duration):
		url = self.discord+"users/@me/guilds/%40me/settings"
		data = {"muted": mute}
		if mute:
			if duration is not None:
				end_time = (datetime.datetime.utcnow()+datetime.timedelta(minutes=duration)).isoformat()[:-3]+'Z'
				data["mute_config"] = {"selected_time_window":duration, "end_time":end_time}
			else:
				data["mute_config"] = {"selected_time_window":-1, "end_time":None}
		body = {"channel_overrides":{str(DMID):data}}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def setThreadNotifications(self, threadID, notifications):
		url = self.discord+"channels/"+threadID+"/thread-members/@me/settings"
		threadNotificationTypes = ["all messages", "only mentions", "nothing"]
		flags = 1<<(self.index(threadNotificationTypes, notifications.lower())+1)
		body = {"flags": flags}
		return Wrapper.sendRequest(self.s, 'patch', url, body, log=self.log)

	def getReportMenu(self):
		url = self.discord+'reporting/menu/first_dm'
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	def reportSpam(self, channelID, messageID, reportType, guildID, version, variant, language):
		url = self.discord+'reporting/'+reportType
		body = {
			"id": calculateNonce(),
			"version": version,
			"variant": variant,
			"language": language,
			"breadcrumbs": [7],
			"elements": {},
			"name": reportType,
			"channel_id": channelID,
			"message_id": messageID,
		}
		if reportType in ('guild_directory_entry', 'stage_channel', 'guild'):
			body["guild_id"] = guildID
		return Wrapper.sendRequest(self.s, 'post', url, body, log=self.log)

	def getHandoffToken(self, key):
		url = self.discord+'auth/handoff'
		body = {"key": key}
		return Wrapper.sendRequest(self.s, 'post', url, body, log=self.log)

	def inviteToCall(self, channelID, userIDs):
		url = self.discord+'channels/'+channelID+'/call/ring'
		body = {"recipients": userIDs}
		return Wrapper.sendRequest(self.s, 'post', url, body, log=self.log)

	def declineCall(self, channelID):
		url = self.discord+'channels/'+channelID+'/call/stop-ringing'
		body = {}
		return Wrapper.sendRequest(self.s, 'post', url, body, log=self.log)

	'''
	Logout
	'''
	def logout(self, provider, voip_provider):
		url = self.discord+"auth/logout"
		body = {"provider": provider, "voip_provider": voip_provider}
		return Wrapper.sendRequest(self.s, 'post', url, body, log=self.log)


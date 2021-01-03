class Event:
	def __init__(self, response):
		self.response = response

	@property
	def ready(self):
		return self.response['t'] == 'READY'

	@property
	def ready_supplemental(self):
		return self.response['t'] == 'READY_SUPPLEMENTAL'

	@property
	def activity_join_request(self): #not sure what this is
		return self.response['t'] == 'ACTIVITY_JOIN_REQUEST'

	@property
	def activity(self): #not sure what this is either
		return self.response['t'] == 'ACTIVITY_START'

	@property
	def braintree(self):
		return self.response['t'] == 'BRAINTREE_POPUP_BRIDGE_CALLBACK'

	@property
	def call(self):
		return self.response['t'] == 'CALL_CREATE'

	@property
	def call_deleted(self):
		return self.response['t'] == 'CALL_DELETE'

	@property
	def call_updated(self):
		return self.response['t'] == 'CALL_UPDATE'

	@property
	def channel(self):
		return self.response['t'] == 'CHANNEL_CREATE'

	@property
	def channel_deleted(self):
		return self.response['t'] == 'CHANNEL_DELETE'

	@property
	def channel_updated(self):
		return self.response['t'] == 'CHANNEL_UPDATE'

	@property
	def channel_read_state_updated(self): #{'t': 'CHANNEL_UNREAD_UPDATE', 's': s, 'op': 0, 'd': {'guild_id': '', 'channel_unread_updates': [{'last_message_id': '', 'id': 'unread id i guess'}, ...]}}
		return self.response['t'] == 'CHANNEL_UNREAD_UPDATE'

	@property
	def pins_ack(self):
		return self.response['t'] == 'CHANNEL_PINS_ACK'

	@property
	def pins_updated(self):
		return self.response['t'] == 'CHANNEL_PINS_UPDATE'

	@property
	def recipient_added(self):
		return self.response['t'] == 'CHANNEL_RECIPIENT_ADD'

	@property
	def recipient_removed(self):
		return self.response['t'] == 'CHANNEL_RECIPIENT_REMOVE'

	@property
	def entitlement(self):
		return self.response['t'] == 'ENTITLEMENT_CREATE'

	@property
	def entitlement_deleted(self):
		return self.response['t'] == 'ENTITLEMENT_DELETE'

	@property
	def entitlement_updated(self):
		return self.response['t'] == 'ENTITLEMENT_UPDATE'

	@property
	def friend_suggestion(self):
		return self.response['t'] == 'FRIEND_SUGGESTION_CREATE'

	@property
	def friend_suggestion_deleted(self):
		return self.response['t'] == 'FRIEND_SUGGESTION_DELETE'

	@property
	def gift_code_updated(self):
		return self.response['t'] == 'GIFT_CODE_UPDATE'

	@property
	def guild_application_commands_updated(self): #huh?
		return self.response['t'] == 'GUILD_APPLICATION_COMMANDS_UPDATE'

	@property
	def ban_added(self): #{'t': 'GUILD_BAN_ADD', 's': s, 'op': 0, 'd': {'user': {'username': username, 'public_flags': 0, 'id': id, 'discriminator': '0000', 'avatar': None}, 'guild_id': guildID}}
		return self.response['t'] == 'GUILD_BAN_ADD'

	@property
	def ban_removed(self):
		return self.response['t'] == 'GUILD_BAN_REMOVE'

	@property
	def guild(self):
		return self.response['t'] == 'GUILD_CREATE'

	@property
	def guild_deleted(self):
		return self.response['t'] == 'GUILD_DELETE'

	@property
	def guild_updated(self):
		return self.response['t'] == 'GUILD_UPDATE'

	@property
	def emojis_updated(self):
		return self.response['t'] == 'GUILD_EMOJIS_UPDATE'

	@property
	def guild_integrations_updated(self):
		return self.response['t'] == 'GUILD_INTEGRATIONS_UPDATE'

	@property
	def guild_member_list(self):
		return self.response['t'] == 'GUILD_MEMBER_LIST_UPDATE'

	@property
	def guild_member_updated(self): #{'t': 'GUILD_MEMBER_UPDATE', 's': s, 'op': 0, 'd': {'user': {'username': usernamd, 'public_flags': 0, 'id': id, 'discriminator': '0000', 'avatar': avatar}, 'roles': [], 'premium_since': None, 'pending': False, 'nick': None, 'joined_at': '', 'is_pending': False, 'guild_id': guildID}}
		return self.response['t'] == 'GUILD_MEMBER_UPDATE'

	@property
	def guild_member_chunk(self): #used for op 8 (when searching in the search bar and members come up)
		return self.response['t'] == 'GUILD_MEMBERS_CHUNK'

	@property
	def role(self):
		return self.response['t'] == 'GUILD_ROLE_CREATE'

	@property
	def role_deleted(self):
		return self.response['t'] == 'GUILD_ROLE_DELETE'

	@property
	def role_updated(self):
		return self.response['t'] == 'GUILD_ROLE_UPDATE'

	@property
	def invite(self):
		return self.response['t'] == 'INVITE_CREATE'

	@property
	def invite_deleted(self):
		return self.response['t'] == 'INVITE_DELETE'

	@property
	def library_app_updated(self):
		return self.response['t'] == 'LIBRARY_APPLICATION_UPDATE'

	@property
	def lobby(self): #idk...https://discord.com/developers/docs/game-sdk/lobbies...
		return self.response['t'] == 'LOBBY_CREATE'

	@property
	def lobby_deleted(self):
		return self.response['t'] == 'LOBBY_DELETE'

	@property
	def lobby_updated(self):
		return self.response['t'] == 'LOBBY_UPDATE'

	@property
	def lobby_member_connected(self):
		return self.response['t'] == 'LOBBY_MEMBER_CONNECT'

	@property
	def lobby_member_disconnected(self):
		return self.response['t'] == 'LOBBY_MEMBER_DISCONNECT'

	@property
	def lobby_member_updated(self):
		return self.response['t'] == 'LOBBY_MEMBER_UPDATE'

	@property
	def lobby_message(self):
		return self.response['t'] == 'LOBBY_MESSAGE'

	@property
	def lobby_voice_server_update(self):
		return self.response['t'] == 'LOBBY_VOICE_SERVER_UPDATE'

	@property
	def lobby_voice_state_update(self):
		return self.response['t'] == 'LOBBY_VOICE_STATE_UPDATE'

	@property
	def message_ack(self): #{'t': 'MESSAGE_ACK', 's': s, 'op': 0, 'd': {'version': v, 'message_id': '', 'channel_id': ''}}
		return self.response['t'] == 'MESSAGE_ACK'

	@property
	def message(self):
		return self.response['t'] == 'MESSAGE_CREATE'

	@property
	def message_deleted(self):
		return self.response['t'] == 'MESSAGE_DELETE'

	@property
	def bulk_messages_deleted(self): #{'t': 'MESSAGE_DELETE_BULK', 's': s, 'op': 0, 'd': {'ids': [], 'channel_id': '', 'guild_id': ''}}
		return self.response['t'] == 'MESSAGE_DELETE_BULK'

	@property
	def reaction_added(self):
		return self.response['t'] == 'MESSAGE_REACTION_ADD'

	@property
	def reaction_removed(self):
		return self.response['t'] == 'MESSAGE_REACTION_REMOVE'

	@property
	def all_message_reactions_removed(self):
		return self.response['t'] == 'MESSAGE_REACTION_REMOVE_ALL'

	@property
	def message_reaction_emoji_removed(self): #not entirely sure what's the difference between this and MESSAGE_REACTION_REMOVE but ok
		return self.response['t'] == 'MESSAGE_REACTION_REMOVE_EMOJI'

	@property
	def message_updated(self):
		return self.response['t'] == 'MESSAGE_UPDATE'

	@property
	def oauth2_token_removed(self): #maybe has to do with deleting an account?
		return self.response['t'] == 'OAUTH2_TOKEN_REMOVE'

	@property
	def presence_replaced(self):
		return self.response['t'] == 'PRESENCES_REPLACE'

	@property
	def presence_updated(self):
		return self.response['t'] == 'PRESENCE_UPDATE'

	@property
	def recent_mention_deleted(self):
		return self.response['t'] == 'RECENT_MENTION_DELETE'

	@property
	def relationship_added(self):
		return self.response['t'] == 'RELATIONSHIP_ADD'

	@property
	def relationship_removed(self):
		return self.response['t'] == 'RELATIONSHIP_REMOVE'

	@property
	def session_replaced(self):
		return self.response['t'] == 'SESSIONS_REPLACE'

	@property
	def stream(self):
		return self.response['t'] == 'STREAM_CREATE'

	@property
	def stream_deleted(self):
		return self.response['t'] == 'STREAM_DELETE'

	@property
	def stream_server_updated(self):
		return self.response['t'] == 'STREAM_SERVER_UPDATE'

	@property
	def stream_updated(self):
		return self.response['t'] == 'STREAM_UPDATE'

	@property
	def typing(self):
		return self.response['t'] == 'TYPING_START'

	@property
	def achievement_updated(self): #idk
		return self.response['t'] == 'USER_ACHIEVEMENT_UPDATE'

	@property
	def connections_updated(self):
		return self.response['t'] == 'USER_CONNECTIONS_UPDATE'

	@property
	def feed_settings_updated(self):
		return self.response['t'] == 'USER_FEED_SETTINGS_UPDATE'

	@property
	def user_guild_settings_updated(self): #like notifications for guilds you're in and that sort of stuff
		return self.response['t'] == 'USER_GUILD_SETTINGS_UPDATE'

	@property
	def note_updated(self):
		return self.response['t'] == 'USER_NOTE_UPDATE'

	@property
	def payment_sources_updated(self):
		return self.response['t'] == 'USER_PAYMENT_SOURCES_UPDATE'

	@property
	def payments_updated(self):
		return self.response['t'] == 'USER_PAYMENTS_UPDATE'

	@property
	def user_premium_guild_sub_slot(self): #now thats a long name
		return self.response['t'] == 'USER_PREMIUM_GUILD_SUBSCRIPTION_SLOT_CREATE'

	@property
	def user_premium_guild_sub_slot_updated(self):
		return self.response['t'] == 'USER_PREMIUM_GUILD_SUBSCRIPTION_SLOT_UPDATE'

	@property
	def required_action_updated(self): #idk
		return self.response['t'] == 'USER_REQUIRED_ACTION_UPDATE'

	@property
	def settings_updated(self): #user settings
		return self.response['t'] == 'USER_SETTINGS_UPDATE'

	@property
	def subscriptions_updated(self):
		return self.response['t'] == 'USER_SUBSCRIPTIONS_UPDATE'

	@property
	def stickers_updated(self):
		return self.response['t'] == 'USER_STICKER_PACK_UPDATE'

	@property
	def user_updated(self):
		return self.response['t'] == 'USER_UPDATE'

	@property
	def voice_server_updated(self):
		return self.response['t'] == 'VOICE_SERVER_UPDATE'

	@property
	def voice_state_updated(self):
		return self.response['t'] == 'VOICE_STATE_UPDATE'

	@property
	def webhooks_updated(self):
		return self.response['t'] == 'WEBHOOKS_UPDATE'


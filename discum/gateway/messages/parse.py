class MessageParse(object):
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
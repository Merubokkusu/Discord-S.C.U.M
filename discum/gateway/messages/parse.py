class MessageParse(object):
	@staticmethod
	def message_create(response):
		message = dict(response["d"])
		types = {
		    0: "default",
		    1: "recipient_added",
		    2: "recipient_removed",
		    3: "call",
		    4: "channel_name_changed",
		    5: "channel_icon_changed",
		    6: "channel_message_pinned",
		    7: "guild_member_joined",
		    8: "user_premium_guild_subscription",
		    9: "user_premium_guild_subscription_tier_1",
		    10: "user_premium_guild_subscription_tier_2",
		    11: "user_premium_guild_subscription_tier_3",
		    12: "channel_follow_added",
		    14: "guild_discovery_disqualified",
		    15: "guild_discovery_requalified",
		    16: "guild_discovery_grace_period_initial_warning",
		    17: "guild_discovery_grace_period_final_warning",
		    18: "thread_created",
		    19: "reply",
		    20: "application_command",
		    21: "thread_starter_message",
		    22: "guild_invite_reminder"
		}
		message["type"] = types[response["d"]["type"]] #number to str
		return message

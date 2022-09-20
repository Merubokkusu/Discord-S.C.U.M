#message types, channel types, etc
#only for objects with the "type" key

class Types:
	msgTypes = {
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
		22: "guild_invite_reminder",
		23: "context_menu_command",
		24: "auto_moderation_action"
	}

	channelTypes = {
		0: "guild_text",
		1: "dm",
		2: "guild_voice",
		3: "group_dm",
		4: "guild_category",
		5: "guild_news",
		6: "guild_store",
		10: "guild_news_thread",
		11: "guild_public_thread",
		12: "guild_private_thread",
		13: "guild_stage_voice",
		14: "guild_directory",
		15: "guild_form"
	}

	relationshipTypes = {
		1: "friend",
		2: "blocked",
		3: "pending_incoming",
		4: "pending_outgoing"
	}

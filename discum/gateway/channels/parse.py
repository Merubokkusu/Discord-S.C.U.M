#parse

class ChannelParse(object): #can either be a guild channel or a DM or something else

	def getChannelType(channelData): #helper method
		types = {
		    0: "guild_text_channel",
		    1: "dm",
		    2: "guild_voice_channel",
		    3: "group_dm",
		    4: "guild_category",
		    5: "guild_news_channel",
		    6: "guild_store_channel"
		}
		return types[channelData["type"]]

	@staticmethod
	def channel_create(response):
		channelData = dict(response["d"])
		channelData["type"] = ChannelParse.getChannelType(channelData)
		if channelData["type"] in ("dm", "group_dm"): #private_channel
			if "recipient_ids" not in channelData and "recipients" in channelData: #should be true, running this check just in case
				channelData["recipient_ids"] = [i["id"] for i in channelData["recipients"]]
		return channelData

	@staticmethod
	def channel_delete(response):
		channelData = dict(response["d"])
		channelData["type"] = ChannelParse.getChannelType(channelData)
		if channelData["type"] in ("dm", "group_dm"): #private_channel
			if "recipient_ids" not in channelData and "recipients" in channelData:
				channelData["recipient_ids"] = [i["id"] for i in channelData["recipients"]]
		return channelData
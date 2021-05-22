from ..types import Types

#parse
class ChannelParse(object): #can either be a guild channel or a DM or something else
	@staticmethod
	def channel_create(response):
		channelData = dict(response["d"])
		channelData["type"] = Types.channelTypes[response["d"]["type"]]
		if channelData["type"] in ("dm", "group_dm"): #private_channel
			if "recipient_ids" not in channelData and "recipients" in channelData: #should be true, running this check just in case
				channelData["recipient_ids"] = [i["id"] for i in channelData["recipients"]]
		return channelData

	@staticmethod
	def channel_delete(response):
		channelData = dict(response["d"])
		channelData["type"] = Types.channelTypes[response["d"]["type"]]
		if channelData["type"] in ("dm", "group_dm"): #private_channel
			if "recipient_ids" not in channelData and "recipients" in channelData:
				channelData["recipient_ids"] = [i["id"] for i in channelData["recipients"]]
		return channelData
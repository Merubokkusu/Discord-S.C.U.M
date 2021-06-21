from ..types import Types
#parses response from gateway

#function names are just lowercase types, so for type GUILD_MEMBER_LIST_UPDATE, the function is guild_member_list_update
class GuildParse(object):
	@staticmethod
	def guild_member_list_update(response):
		memberdata = {
		    "online_count": response["d"]["online_count"],
		    "member_count": response["d"]["member_count"],
		    "id": response["d"]["id"],
		    "guild_id": response["d"]["guild_id"],
		    "hoisted_roles": response["d"]["groups"],
		    "types": [],
		    "locations": [],
		    "updates": []
		}
		#now time to look over ops
		for chunk in response['d']['ops']:
			memberdata['types'].append(chunk['op'])
			if chunk['op'] in ('SYNC', 'INVALIDATE'):
				memberdata['locations'].append(chunk['range'])
				if chunk['op'] == 'SYNC':
					memberdata['updates'].append(chunk['items'])
				else: #invalidate
					memberdata['updates'].append([])
			elif chunk['op'] in ('INSERT', 'UPDATE', 'DELETE'): #only update the 0,99 range btw
				memberdata['locations'].append(chunk['index'])
				if chunk['op'] == 'DELETE':
					memberdata['updates'].append([])
				else:
					memberdata['updates'].append(chunk['item'])
		#and that's it. mostly some renaming and shuffling around to help with usage and reading :)
		return memberdata

	@staticmethod
	def guild_create(response, my_user_id):
		guilddata = dict(response["d"])
		#take care of position
		guilddata["my_data"] = response["d"].get("members", [])
		guilddata["members"] = {} #we dont actually get sent the member list from guild creates. however, this usually contains our position/role in that guild so...still good info
		guilddata["my_data"] = next((a for a in guilddata["my_data"] if a["user"]["id"]==my_user_id), {})
		if len(guilddata["my_data"]) == 1:
			guilddata["my_data"][0].pop("user", None)
			guilddata["my_data"][0]["user_id"] = my_user_id
		#take care of emojis
		guilddata["emojis"] = {i["id"]:i for i in response["d"]["emojis"]}
		#take care of roles
		guilddata["roles"] = {j["id"]:j for j in response["d"]["roles"]}
		#take care of channels
		guilddata["channels"] = {k["id"]:dict(k,**{"type":Types.channelTypes[k["type"]]}) for k in response["d"]["channels"]}
		return guilddata

	@staticmethod
	def guild_members_chunk(response):
		memberChunkData = {"members":[], "guild_id": response["d"]["guild_id"], "chunk_count":response["d"]["chunk_count"], "chunk_index":response["d"]["chunk_index"]}
		if "not_found" in response["d"]:
			memberChunkData["not_found"] = [str(n) for n in response["d"]["not_found"]] #list of user ids
		presences = {}
		if "presences" in response["d"]:
			presences = {i["user"]["id"]:i for i in response["d"]["presences"]}
		for user in response["d"]["members"]:
			completeData = dict(user) 
			defaultPresence = {"user": {"id": user.get("user").get("id")}, "status": "offline", "client_status": {}, "activities": []} #offline status
			completeData["presence"] = presences.pop(user.get("user").get("id"), defaultPresence)
			memberChunkData["members"].append(completeData)
		return memberChunkData

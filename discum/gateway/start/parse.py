from ..types import Types

#parse (remember to do static methods, unless you're changing the formatting)
class StartParse(object): #really hope this doesn't take too long to run...
	@staticmethod
	def ready(response):
		ready_data = dict(response["d"])
		ready_data.pop("merged_members")
		#parse relationships
		ready_data["relationships"] = {i["id"]:dict(i,**{"type":Types.relationshipTypes[i["type"]]}) for i in response["d"]["relationships"]}
		#parse private channels
		ready_data["private_channels"] = {j["id"]:dict(j,**{"type":Types.channelTypes[j["type"]]}) for j in response["d"]["private_channels"]}
		#add activities key to user settings
		ready_data["user_settings"]["activities"] = {}
		#parse guilds
		guilds = response["d"]["guilds"]
		ready_data["guilds"] = {k["id"]:k for k in guilds}
		for personal_role, guild in zip(response["d"]["merged_members"], guilds):
			if "unavailable" not in ready_data["guilds"][guild["id"]]:
				#take care of emojis
				if isinstance(guild["emojis"], list):
					ready_data["guilds"][guild["id"]]["emojis"] = {l["id"]:l for l in guild["emojis"]}
				#take care of roles
				if isinstance(guild["roles"], list):
					ready_data["guilds"][guild["id"]]["roles"] = {m["id"]:m for m in guild["roles"]}
				#take care of channels
				if isinstance(guild["channels"], list):
					ready_data["guilds"][guild["id"]]["channels"] = {n["id"]:dict(n,**{"type":Types.channelTypes[n["type"]]}) for n in guild["channels"]}
			#take care of personal role/nick
			ready_data["guilds"][guild["id"]]["my_data"] = next((i for i in personal_role if i["user_id"]==response["d"]["user"]["id"]), {}) #personal_role
			#take care of members
			ready_data["guilds"][guild["id"]]["members"] = {}
		return ready_data

	@staticmethod
	def ready_supplemental(response):
		ready_supp_data = dict(response["d"])
		ready_supp_data["online_friends"] = {o["user_id"]:o for o in response["d"]["merged_presences"]["friends"]}
		ready_supp_data.pop("guilds")
		ready_supp_data["voice_states"] = {p["id"]:p.get("voice_states",[]) for p in response["d"]["guilds"]} #id is the guild_id
		return ready_supp_data

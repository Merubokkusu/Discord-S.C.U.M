#parse (remember to do static methods, unless you're changing the formatting)

class StartParse(object): #really hope this doesn't take too long to run...
	@staticmethod
	def ready(response):
		ready_data = dict(response["d"])
		ready_data.pop("merged_members")
		#parse relationships
		ready_data["relationships"] = {i["id"]:i for i in response["d"]["relationships"]}
		#parse private channels
		ready_data["private_channels"] = {j["id"]:j for j in response["d"]["private_channels"]}
		#add activities key to user settings
		ready_data["user_settings"]["activities"] = {}
		#parse guilds
		guilds = response["d"]["guilds"]
		ready_data["guilds"] = {k["id"]:k for k in guilds}
		for personal_role, guild in zip(response["d"]["merged_members"], guilds):
			#take care of personal role/nick
			ready_data["guilds"][guild["id"]]["my_data"] = personal_role
			#take care of emojis
			ready_data["guilds"][guild["id"]]["emojis"] = {l["id"]:l for l in guild["emojis"]}
			#take care of roles
			ready_data["guilds"][guild["id"]]["roles"] = {m["id"]:m for m in guild["roles"]}
			#take care of channels
			ready_data["guilds"][guild["id"]]["channels"] = {n["id"]:n for n in guild["channels"]}
			#take care of members
			ready_data["guilds"][guild["id"]]["members"] = {}
		return ready_data

	@staticmethod
	def ready_supplemental(response):
		ready_supp_data = dict(response["d"])
		ready_supp_data["online_friends"] =  {o["user_id"]:o for o in response["d"]["merged_presences"]["friends"]}
		ready_supp_data.pop("guilds")
		ready_supp_data["voice_states"] = {p["id"]:p["voice_states"] for p in response["d"]["guilds"]} #id is the guild_id
		return ready_supp_data
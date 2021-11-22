#points to commands that help request info/actions using the gateway

class GuildRequest(object):
	__slots__ = ['gatewayobj']
	def __init__(self, gatewayobj):
		self.gatewayobj = gatewayobj

	def lazyGuild(self, guild_id, channel_ranges, typing, threads, activities, members, thread_member_lists): #https://arandomnewaccount.gitlab.io/discord-unofficial-docs/lazy_guilds.html
		data = {
		    "op": self.gatewayobj.OPCODE.LAZY_REQUEST,
		    "d": {
		        "guild_id": guild_id,
		        "typing": typing,
		        "threads": threads,
		        "activities": activities,
		        "members": members,
		        "channels": channel_ranges,
		        "thread_member_lists": thread_member_lists
		    },
		}
		if channel_ranges == None:
			data["d"].pop("channels")
		if typing == None:
			data["d"].pop("typing")
		if threads == None:
			data["d"].pop("threads")
		if activities == None:
			data["d"].pop("activities")
		if members == None:
			data["d"].pop("members")
		if thread_member_lists == None:
			data["d"].pop("thread_member_lists")
		self.gatewayobj.send(data)

	def searchGuildMembers(self, guild_ids, query, limit, presences, user_ids, nonce): #note that query can only be "" if you have admin perms (otherwise you'll get inconsistent responses from discord)
		if isinstance(guild_ids, str):
			guild_ids = [guild_ids]
		data = {
		    "op": self.gatewayobj.OPCODE.REQUEST_GUILD_MEMBERS,
		    "d": {"guild_id": guild_ids},
		}
		if isinstance(user_ids, list): #there are 2 types of op8 that the client can send
			data["d"]["user_ids"] = user_ids
		else:
			data["d"]["query"] = query
			data["d"]["limit"] = limit
		if presences != None:
			data["d"]["presences"] = presences
		if nonce != None:
			data["d"]["nonce"] = nonce
		self.gatewayobj.send(data)

	#wait but why is this under guild? because gateway slash command searching only works in guilds
	#example "d" fields (from client):
	'''
	{"guild_id": "blah", "nonce": "blah", "type": 1, "limit": 7, "query": "test"}
	{"guild_id": "blah", "nonce": "blah", "type": 1, "applications": True, "offset": 0, "command_ids": ["blah", ...], "limit":10}
	{"guild_id": "blah", "nonce": "blah", "type": 1, "offset": 30, "limit": 10}
	'''
	def searchSlashCommands(self, guild_id, query, command_ids, applicationID, limit, offset, nonce, appType):
		#nonce
		if nonce == "calculate":
			from ...utils.nonce import calculateNonce
			nonce = calculateNonce()
		else:
			nonce = str(nonce)

		#payload
		data = {
			"op": self.gatewayobj.OPCODE.REQUEST_APPLICATION_COMMANDS,
			"d": {"guild_id": guild_id, "nonce": nonce, "type": 1},
		}

		#application type
		appType = appType.lower()
		if 'user' in appType:
			data["d"]["type"] = 2
		elif 'message' in appType:
			data["d"]["type"] = 3

		#case 1: search by query
		if query != None:
			data["d"].update({"limit":limit, "query":query})
			if offset != None:
				data["d"]["offset"] = offset
		#case 2: search by command ids
		elif command_ids != None:
			if isinstance(command_ids, str):
				command_ids = [command_ids]
			data["d"].update({"applications":True, "offset":0 if offset==None else offset, "command_ids":command_ids, "limit":limit})
		#case 3: get them all (with a limit)
		else:
			data["d"]["limit"] = limit
			if offset != None:
				data["d"]["offset"] = offset

		#idk, this isn't ever done in the client but it's useful so here goes
		if applicationID != None:
			data["d"]["application_id"] = applicationID
		self.gatewayobj.send(data)
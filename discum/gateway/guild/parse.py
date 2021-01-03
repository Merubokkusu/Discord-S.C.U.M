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
				


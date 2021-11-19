#x-context-properties
#some of these values are hardcoded cause that's just faster

import base64
import json

class ContextProperties(object):
	@staticmethod
	def encodeData(data):
		binaryData = json.dumps(data).encode()
		encodedData = base64.b64encode(binaryData).decode("utf-8")
		return encodedData

	@staticmethod
	def get(location, guild_id=None, channel_id=None, channel_type=None):
		loc = location.lower()
		if loc == "friends":
			return "eyJsb2NhdGlvbiI6IkZyaWVuZHMifQ==" # {"location":"Friends"}
		elif loc == "context menu":
			return "eyJsb2NhdGlvbiI6IkNvbnRleHRNZW51In0=" # {"location":"ContextMenu"}
		elif loc == "user profile":
			return "eyJsb2NhdGlvbiI6IlVzZXIgUHJvZmlsZSJ9" # {"location":"User Profile"}
		elif loc == "add friend":
			return "eyJsb2NhdGlvbiI6IkFkZCBGcmllbmQifQ==" # {"location":"Add Friend"}
		elif loc == "new group dm":
			return "eyJsb2NhdGlvbiI6Ik5ldyBHcm91cCBETSJ9" # {"location":"New Group DM"}
		elif loc == "add friends to dm":
			return "eyJsb2NhdGlvbiI6IkFkZCBGcmllbmRzIHRvIERNIn0=" # {"location":"Add Friends to DM"}
		elif loc == "group dm invite create":
			return "eyJsb2NhdGlvbiI6Ikdyb3VwIERNIEludml0ZSBDcmVhdGUifQ==" # {"location":"Group DM Invite Create"}
		elif loc == "school hub guild":
			return "eyJzb3VyY2UiOiJEaXJlY3RvcnkgQ2hhbm5lbCBFbnRyeSJ9" # {"source":"Directory Channel Entry"}
		elif loc == "school hub sidebar":
			return "eyJsb2NhdGlvbiI6Ikh1YiBTaWRlYmFyIn0=" # {"location":"Hub Sidebar"}
		elif loc == "guild header":
			return "eyJsb2NhdGlvbiI6Ikd1aWxkIEhlYWRlciJ9" # {"location":"Guild Header"}
		elif loc == "markdown":
			return "eyJsb2NhdGlvbiI6Ik1hcmtkb3duIExpbmsifQ==" # {"location":"Markdown Link"}
		elif loc in ("accept invite page", "join guild"):
			data = {
				"location": loc.title(),
				"location_guild_id": guild_id,
				"location_channel_id": channel_id,
				"location_channel_type": channel_type,
			}
			if loc == "join guild":
				data["location"] = "Join Guild"
			return ContextProperties.encodeData(data)
		else:
			data = {"location":location}
			return ContextProperties.encodeData(data)
class SlashCommander(object):
	__slots__ = ['commands', 'option_types']
	def __init__(self, commands, application_id=None):
		if isinstance(commands, dict):
			if application_id == None:
				self.commands = {"options":[commands]}
			else:
				self.commands = {"options":[commands if commands["application_id"]==application_id else {}]}
		elif type(commands) in (list, tuple) and isinstance(commands[0], dict):
			if application_id == None:
				self.commands = {"options":commands}
			else:
				self.commands = {"options":[cmd for cmd in commands if cmd["application_id"]==application_id]}
		else:
			raise ValueError("commands must be either a list of dicts or a dict.")

		self.option_types = {
			1: ("SUB_COMMAND", None),
			2: ("SUB_COMMAND_GROUP", None),
			3: ("STRING", str),
			4: ("INTEGER", int),
			5: ("BOOLEAN", bool),
			6: ("USER", str),
			7: ("CHANNEL", str),
			8: ("ROLE", str),
			9: ("MENTIONABLE", str),
			10: ("NUMBER", float)
		}

	#gets sub-dictionary from command list input
	def _getCmdSubdict(self, cmdList):
		result = self.commands
		for cmd in cmdList:
			result = next(
				(
					c for c in result["options"]
					if c["name"] == cmd and (c["type"] in (1, 2) or self._isAtOuterLvl(c))
				),
				None,
			)
			if result == None:
				raise ValueError("{} is not a valid command list".format(cmdList))
		return result

	#gets subdictionary pointer from constructed/input dictionary
	def _getConstructedSubdict(self, inputDict, depth):
		result = inputDict
		for i in range(depth):
			if len(result["options"]) == 0:
				result["options"].append({})
			result = result["options"][0]
		return result

	#check if at the outer level of the command
	def _isAtOuterLvl(self, inputDict):
		return "version" in inputDict

	#get type, description, and options of command (from command list)
	def metadata(self, cmdList):
		theDict = self._getCmdSubdict(cmdList)
		m = {
			"type": self.option_types[theDict["type"]][0],
			"description": theDict.get("description"),
		}
		if m["type"] in ("SUB_COMMAND", "SUB_COMMAND_GROUP"):
			m["options"] = [i for i in theDict.get("options", [])]
		return m

	#get options (attributes and parameters) of command (from command list)
	def options(self, cmdList):
		theDict = self._getCmdSubdict(cmdList)
		if theDict["type"] in (1, 2) or self._isAtOuterLvl(theDict):
			options = [
				dict(i, **{"type": self.option_types[i["type"]][0]})
				for i in theDict.get("options", [])
			]
			return options

	#get constructed slash command data
	def get(self, cmdList, inputs={}):
		constructed_slash_cmd = {}
		current_cmd = self.commands
		for index, cmd in enumerate(cmdList):
			current_cmd = next(
				(
					c for c in current_cmd["options"]
					if c["name"] == cmd and c["type"] in (1, 2)
				),
				None
			)
			if current_cmd == None:
				raise ValueError("{} is not a valid command list".format(cmdList))
			data = {
					"name": current_cmd["name"],
					"type": current_cmd["type"],
					"options": []
			}
			if self._isAtOuterLvl(current_cmd):
				data.update(
					{
						"version": current_cmd.get("version"),
						"id": current_cmd["id"],
						"attachments": [], #only the top layer of cmds has attachments
						"application_command": dict(current_cmd)
					}
				)
			self._getConstructedSubdict(constructed_slash_cmd, index).update(data)
		options = self._getCmdSubdict(cmdList).get("options", [])
		constructed_option_data = []
		for param in inputs:
			param_link = next((item for item in options if item["name"] == param), None)
			if param_link:
				correct_type = self.option_types[param_link["type"]][1]
				constructed_option_data.append(
					{
						"type": param_link["type"],
						"name": param_link["name"],
						"value": correct_type(inputs[param]),
					}
				)
		self._getConstructedSubdict(constructed_slash_cmd, len(cmdList)-1).update({"options":constructed_option_data})
		return constructed_slash_cmd


'''
from slash import SlashCommander
import json

s = SlashCommander(test)
s.options(['saved', 'queues', 'delete'])
s.metadata(['saved', 'queues'])
s.get(['saved', 'queues', 'delete'], {'name':'poop'})
s.get(['choose'], {'1st':1, '2nd':2})
'''

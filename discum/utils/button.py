#https://stackoverflow.com/a/44250949, works in python 2 and 3
def zip_longest(*lists):
	def g(l):
		for item in l:
			yield item
		while True:
			yield None
	gens = [g(l) for l in lists]    
	for _ in range(max(map(len, lists))):
		yield tuple(next(g) for g in gens)
# get a list of buttons wether they have labels or they made of emojis, while being able to exclude buttons that are non clickable
def getButtons(message, exculde_disabled=False) :
	for component in message["components"] :
		if component["type"]==1 :
			buttons=[]
			for button in component["components"] :
				if button["type"]==2 and ("disabled" not in button or not exculde_disabled) :
					if "label" in button : buttons.append(button["label"])
					elif "emoji" in button : buttons.append(button["emoji"]["name"])
			return buttons
			return [button["label"] for button in component["components"] if button["type"]==2 and ("disabled" not in button or not exculde_disabled)]
	return []
#press a button as easy as possible
def pressButton(bot : discum.Client, message, target, using_emoji=False, refresh_afterwards=False) :
	buts = Buttoner(message["components"])
	if type(target)==int : target=getButtons(message)[target] #press a button based on where it is
	if using_emoji : data=buts.getButton(emojiName=target)
	else : data=buts.getButton(target)
	if "guild_id" in message : guild_id=message["guild_id"]
	else :
		try : guild_id=message["message_reference"]["guild_id"] # if there is a referenced message then the guild id will only exist there
		except : guild_id = None
	pressresponce=bot.click(
		message["author"]["id"],
		channelID=message["channel_id"],
		guildID=guild_id,
		messageID=message["id"],
		messageFlags=message["flags"],
		data=data,
	)
	#most of the time the message gets edited after pressing a butoon so you would want to get the new contents of it
	if refresh_afterwards :
		from time import sleep
		sleep(2) #waiting a while between pressing and getting the message
		return list(bot.getMessage(message["channel_id"], message["id"]).json())[0]
	return pressresponce
class Buttoner(object):
	__slots__ = ['components', 'component_types']
	def __init__(self, components):
		if (type(components) in (list, tuple) 
		and (len(components) == 0 or isinstance(components[0], dict))):
			self.components = list(dict(i) for i in components)
		else:
			raise ValueError("components must be a list of dicts.")

		self.component_types = {
			1: "ACTION_ROW",
			2: "BUTTON",
			3: "SELECT_MENU"
		}

	#check stuff, inputs are [a, b, c, d, ...] and ['a', 'b', 'c', 'd', ...]
	def _check(self, inputs, stuffToCheck):
		if all(i is None for i in inputs):
			return False
		for index,i in enumerate(inputs):
			if i != None:
				if i != stuffToCheck[index]:
					return False
		return True

	#get attributes of a button
	def findButton(self, label=None, customID=None, row=None, column=None, emojiName=None, emojiID=None, findFirst=False):
		buttons = []
		#row
		if row != None:
			data = [self.components[row]]
		else:
			data = self.components
		#loop
		for row in data:
			for index,c in enumerate(row["components"]):
				#if button
				if c["type"] == 2:
					if self._check(
						[label, customID, column, emojiName, emojiID],
						[
							c.get("label"),
							c["custom_id"],
							index,
							c.get("emoji", {}).get("name"),
							c.get("emoji", {}).get("id"),
						],
					):
						buttons.append(dict(c))
						if findFirst:
							return buttons
		return buttons


	#get attributes of a menu
	def findMenu(self, placeholder=None, customID=None, row=None, findFirst=False): #placeholder, customID, row
		menus = []
		#row
		if row != None:
			data = [self.components[row]] #only 1 menu per role, but still need to check the other parameters
		else:
			data = self.components
		#loop
		for row in data:
			for c in row["components"]:
				#if menu
				if c["type"] == 3:
					if self._check([placeholder, customID], [c.get("placeholder", "Make a selection"), c["custom_id"]]):
						menus.append(dict(c))
						if findFirst:
							return menus
		return menus

	def findDropdown(self, menu, label=None, description=None, value=None, emojiName=None, emojiID=None, findFirst=False): #label, description, value, emojiName, emojiID
		dropdowns = []
		for option in menu["options"]:
			if self._check(
				[label, description, value, emojiName, emojiID],
				[
					option["label"],
					option.get("description"),
					option["value"],
					option.get("emoji", {}).get("name"),
					option.get("emoji", {}).get("id"),
				],
			):
				dropdowns.append(dict(option))
				if findFirst:
					return dropdowns
		return dropdowns

	#get constructed button data
	def getButton(self, label=None, customID=None, row=None, column=None, emojiName=None, emojiID=None):
		button = self.findButton(label, customID, row, column, emojiName, emojiID, findFirst=True)
		if len(button)>0:
			return {"component_type": 2, "custom_id": button[0]["custom_id"]}
		else:
			raise ValueError("Button with inputted attributes not found.")

	#get constructed menu data
	def getMenuSelection(self, placeholder=None, customID=None, row=None, labels=[], descriptions=[], values=[], emojiNames=[], emojiIDs=[]):
		menu = self.findMenu(placeholder, customID, row, findFirst=True)
		if len(menu)>0:
			menuData = {"component_type":3, "custom_id":menu[0]["custom_id"], "values":[]}
			for l,d,v,eN,eID in zip_longest(labels, descriptions, values, emojiNames, emojiIDs):
				dropdown = self.findDropdown(menu[0], label=l, description=d, value=v, emojiName=eN, emojiID=eID)
				if len(dropdown)>0:
					menuData["values"].append(dropdown[0]["value"])
			return menuData
		else:
			raise ValueError("Menu with inputted attributes not found.")

'''
from button import Buttoner
b = Buttoner(...)
but = b.getButton(label="Moose")
bot.click(but)
but = b.getMenuSelection(row=3, labels=["car", "bus", "train"])
bot.click(but)

b.findButton()
b.findMenu()
b.findDropdown()
'''
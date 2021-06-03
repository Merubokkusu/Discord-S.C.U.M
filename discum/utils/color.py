import random

'''
sources:
https://github.com/Rapptz/discord.py/blob/master/discord/colour.py
https://discord.com/branding
https://gist.github.com/thomasbnt/b6f455e2c7d743b796917fa3c205f812
'''

class Color:
	colors = {
		"black": 0,
		"default": 0, #just another name for black ig
		"aqua": 0x1ABC9C,
		"teal": 0x1ABC9C, #same as aqua
		"dark_aqua": 0x11806A,
		"dark_teal": 0x11806A, #same as dark_aqua
		"green": 0x2ECC71,
		"dark_green": 0x1F8B4C,
		"blue": 0x3498DB,
		"dark_blue": 0x206694,
		"purple": 0x9B59B6,
		"dark_purple": 0x71368A,
		"magenta": 0xE91E63,
		"luminous_vivid_pink": 0xE91E63, #same as magenta
		"dark_magenta": 0xAD1457,
		"dark_vivid_pink": 0xAD1457, #same as dark_magenta
		"gold": 0xF1C40F,
		"dark_gold": 0xC27C0E,
		"orange": 0xE67E22,
		"dark_orange": 0xA84300,
		"red": 0xE74c3C,
		"dark_red": 0x992D22,
		"light_grey": 0xBCC0C0,
		"grey": 0x95A5A6,
		"dark_grey": 0x979C9F,
		"darker_grey": 0x7F8C8D,
		"og_blurple": 0x7289DA,
		"ruined_blurple": 0x586AEA,
		"blurple": 0x5865F2,
		"greyple": 0x99AAB5,
		"dark_theme": 0x36393F,
		"not_quite_black": 0x23272A,
		"dark_but_not_black": 0x2C2F33,
		"white": 0xFFFFFE, #thx dolfies for noting that 0xFFFFFF doesn't work
		"fuchsia": 0xEB459E,
		"yellow": 0xFEE75C,
		"navy": 0x34495E,
		"dark_navy": 0x2C3E50
	}

	@staticmethod
	def get_random_color():
		return random.randint(0x000000, 0xFFFFFF)

	@staticmethod
	def get_byte(value, byte):
		return (value >> (8*byte)) & 0xFF

	@staticmethod
	def from_rgb(*args):
		newArgs = [0,0,0]
		if type(args[0]) in (list, tuple):
			newArgs[0],newArgs[1],newArgs[2] = args[0]
		else:
			newArgs = list(args)
		return (newArgs[0]<<16) + (newArgs[1]<<8) + newArgs[2]

	@staticmethod
	def to_rgb(c):
		return (Color.get_byte(c,2), Color.get_byte(c,1), Color.get_byte(c,0))

	@staticmethod
	def get(*args): #accepts decimal, hex, rgb
		#args -> c
		if len(args) == 3:
			c = args
		elif len(args) == 1:
			c = args[0]
		else:
			raise ValueError("Expected either decimal, hex, or rgb input.")
		#parse c (color input)
		if isinstance(c, tuple) or isinstance(c, list):
			result = Color.from_rgb(c)
		elif isinstance(c, str):
			if c.startswith("0x"):
				result = int(c, 0)
			else:
				c = c.lower()
				if c == "random":
					result = Color.get_random_color()
				else:
					key = c.replace("gray", "grey")
					if key in Color.colors:
						result = Color.colors[key]
					else:
						result = int(c, 16)
		else:
			result = c
		return result
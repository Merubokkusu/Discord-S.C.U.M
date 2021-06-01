#those accessibility numbers that discord uses for its "science"

class ACCESSIBILITY_FEATURES:
	SCREENREADER = 1 << 0
	REDUCED_MOTION = 1 << 1
	REDUCED_TRANSPARENCY = 1 << 2
	HIGH_CONTRAST = 1 << 3
	BOLD_TEXT = 1 << 4
	GRAYSCALE = 1 << 5
	INVERT_COLORS = 1 << 6
	PREFERS_COLOR_SCHEME_LIGHT = 1 << 7
	PREFERS_COLOR_SCHEME_DARK = 1 << 8
	CHAT_FONT_SCALE_INCREASED = 1 << 9
	CHAT_FONT_SCALE_DECREASED = 1 << 10
	ZOOM_LEVEL_INCREASED = 1 << 11
	ZOOM_LEVEL_DECREASED = 1 << 12
	MESSAGE_GROUP_SPACING_INCREASED = 1 << 13
	MESSAGE_GROUP_SPACING_DECREASED = 1 << 14
	DARK_SIDEBAR = 1 << 15
	REDUCED_MOTION_FROM_USER_SETTINGS = 1 << 16

class Accessibility:
	@staticmethod
	def calculateAccessibility(types):
		accessibilityNum = 0
		for i in types:
			feature = i.upper().replace(" ", "_")
			if hasattr(ACCESSIBILITY_FEATURES, feature):
				accessibilityNum |= getattr(ACCESSIBILITY_FEATURES, feature)
		return accessibilityNum

	@staticmethod
	def checkAccessibilities(accessibilityNum, check):
		return (accessibilityNum & check) == check

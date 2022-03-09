#handles building the superproperties dictionary. also includes getting the build number (since this is part of the super properties)

import ua_parser.user_agent_parser
import re
import time

from ..RESTapiwrap import Wrapper
from ..logger import Logger

class SuperProperties:
	'''
	https://luna.gitlab.io/discord-unofficial-docs/science.html#super-properties-object
	'''
	__slots__ = ['s', 'editedS', 'buildnum', 'log']
	def __init__(self, s, buildnum="request", log={"console":True, "file":False}):
		self.s = s
		self.editedS = Wrapper.editedReqSession(s, {"remove": ["Authorization", "X-Super-Properties", "X-Fingerprint"]})
		self.buildnum = buildnum
		self.log = log

	def requestBuildNumber(self):
		Logger.log("Retrieving Discord's build number...", None, self.log) 
		try: #getting the build num is kinda experimental since who knows if discord will change where the build number is located...
			extraMods = {"update":{"Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate","Sec-Fetch-Site": "none"}}
			

			res = Wrapper.sendRequest(self.editedS, 'get', "https://discord.com/login", headerModifications=extraMods, log=False)
			if res:
				self.s.cookies.update(res.cookies)
			discord_login_page_exploration = res.text

			#fastest solution I could find since the last js file is huge in comparison to 2nd from last
			file_with_build_num = 'https://discord.com/assets/'+re.compile(r'assets/+([a-z0-9]+)\.js').findall(discord_login_page_exploration)[-2]+'.js'
			req_file_build = Wrapper.sendRequest(self.editedS, 'get', file_with_build_num, log=False).text #log set to False cause this is a big file
			index_of_build_num = req_file_build.find('buildNumber')+24
			discord_build_num = int(req_file_build[index_of_build_num:index_of_build_num+6])

			Logger.log('Discord is currently on build number '+str(discord_build_num), None, self.log)
			return discord_build_num
		except Exception as e:
			Logger.log('Could not retrieve discord build number.', None, self.log)
			Logger.log(e, None, self.log)
			return None

	def getSuperProperties(self, user_agent, locale):
		parseduseragent = ua_parser.user_agent_parser.Parse(user_agent)
		browser_ver_list = [parseduseragent["user_agent"]["major"], parseduseragent["user_agent"]["minor"], parseduseragent["user_agent"]["patch"]]
		os_ver_list = [parseduseragent["os"]["major"], parseduseragent["os"]["minor"], parseduseragent["os"]["patch"]]
		sp = {
			"os": parseduseragent["os"]["family"],
			"browser": parseduseragent["user_agent"]["family"],
			"device": "",
			"system_locale": locale,
			"browser_user_agent": parseduseragent["string"],
			"browser_version": ".".join(filter(None, browser_ver_list)),
			"os_version": ".".join(filter(None, os_ver_list)),
			"referrer": "",
			"referring_domain": "",
			"referrer_current": "",
			"referring_domain_current": "",
			"release_channel": "stable",
			"client_build_number": 117300,
			"client_event_source": None
		}
		if locale == None:
			sp.pop("system_locale")
		if self.buildnum == "request":
			reqbuildnum = self.requestBuildNumber()
			if reqbuildnum != None:
				sp["client_build_number"] = reqbuildnum
		else:
			sp["client_build_number"] = int(self.buildnum)
		return sp

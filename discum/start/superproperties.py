#handles building the superproperties dictionary. also includes getting the build number (since this is part of the super properties)

import ua_parser.user_agent_parser
import re
import time

class SuperProperties:
    '''
    https://luna.gitlab.io/discord-unofficial-docs/science.html#super-properties-object
    '''
    def __init__(self, s, buildnum="request", log=True):
        self.s = s
        self.buildnum = buildnum
        self.log = log

    def RequestBuildNumber(self):
        if self.log: print("Retrieving Discord's build number...")
        discord_login_page_exploration = self.s.get('https://discord.com/login').text
        time.sleep(1)
        try: #getting the build num is kinda experimental since who knows if discord will change where the build number is located...
            file_with_build_num = 'https://discord.com/assets/'+re.compile(r'assets/+([a-z0-9]+)\.js').findall(discord_login_page_exploration)[-2]+'.js' #fastest solution I could find since the last js file is huge in comparison to 2nd from last
            req_file_build = self.s.get(file_with_build_num).text
            index_of_build_num = req_file_build.find('buildNumber')+14
            discord_build_num = int(req_file_build[index_of_build_num:index_of_build_num+5])
            if self.log: print('Discord is currently on build number '+str(discord_build_num))
            return discord_build_num
        except:
            if self.log: print('Could not retrieve discord build number.')
            return None

    def GetSuperProperties(self, user_agent):
        parseduseragent = ua_parser.user_agent_parser.Parse(user_agent)
        browser_ver_list = [parseduseragent["user_agent"]["major"], parseduseragent["user_agent"]["minor"], parseduseragent["user_agent"]["patch"]]
        os_ver_list = [parseduseragent["os"]["major"], parseduseragent["os"]["minor"], parseduseragent["os"]["patch"]]
        sp = {
            "os": parseduseragent["os"]["family"],
            "browser": parseduseragent["user_agent"]["family"],
            "device": "",
            "browser_user_agent": parseduseragent["string"],
            "browser_version": ".".join(filter(None, browser_ver_list)),
            "os_version": ".".join(filter(None, os_ver_list)),
            "referrer": "",
            "referring_domain": "",
            "referrer_current": "",
            "referring_domain_current": "",
            "release_channel": "stable",
            "client_build_number": 73777,
            "client_event_source": None
        }
        if self.buildnum == "request":
            reqbuildnum = self.RequestBuildNumber()
            if reqbuildnum != None:
                sp["client_build_number"] = reqbuildnum
        elif isinstance(self.buildnum, int):
            sp["client_build_number"] = self.buildnum
        return sp

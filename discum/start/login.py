from ..RESTapiwrap import *
from ..utils.totp import TOTP
from ..utils.contextproperties import ContextProperties
import time

from ..logger import Logger

class Login:
	'''
	Manages HTTP authentication
	'''
	__slots__ = ['discord', 'log', 'editedS', 'xfingerprint']
	def __init__(self, s, discordurl, log):
		self.discord = discordurl
		self.log = log
		self.editedS = Wrapper.editedReqSession(s, {"remove": ["Authorization", "X-Fingerprint"]})

	def getXFingerprint(self):
		url = self.discord + "experiments"
		reqxfinger = Wrapper.sendRequest(self.editedS, 'get', url, headerModifications={"update":{"X-Context-Properties":ContextProperties.get("/app")}}, log=self.log)
		xfingerprint = reqxfinger.json().get('fingerprint')
		if not xfingerprint:
			Logger.log('xfingerprint could not be fetched.', None, self.log)
		return xfingerprint

	def login(self, email, password, undelete, captcha, source, gift_code_sku_id, secret, code):
		url = self.discord + "auth/login"
		self.xfingerprint = self.getXFingerprint()
		self.editedS.headers.update({"X-Fingerprint": self.xfingerprint})
		body = {
			"email": email,
			"password": password,
			"undelete": undelete,
			"captcha_key": captcha,
			"login_source": source,
			"gift_code_sku_id": gift_code_sku_id
		}
		response = Wrapper.sendRequest(self.editedS, 'post', url, body, log=self.log)
		result = response.json()
		if result.get('mfa') == True and result.get('sms') == False: #sms login not implemented yet
			time.sleep(2) #2 seconds is minimal, don't want to look too automated
			ticket = result['ticket']
			if secret != "":
				code = TOTP(secret).generateTOTP()
			code = str(code) #just in case an int is inputted
			totpUrl = self.discord+"auth/mfa/totp"
			totpBody = {
				"code": code,
				"ticket": ticket,
				"login_source": source,
				"gift_code_sku_id": gift_code_sku_id
			}
			totpResponse = Wrapper.sendRequest(self.editedS, 'post', totpUrl, totpBody, log=self.log)
			return totpResponse, self.xfingerprint
		else:
			return response, self.xfingerprint

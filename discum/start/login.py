import time

from ..RESTapiwrap import Wrapper
from ..logger import Logger

from ..utils.totp import TOTP
from ..utils.contextproperties import ContextProperties
from ..utils.nonce import calculateNonce

class Login:
	'''
	Manages HTTP authentication
	'''
	__slots__ = ['discord', 'log', 'editedS', 'xfingerprint']
	def __init__(self, s, discordurl, log):
		self.discord = discordurl
		self.log = log
		self.editedS = Wrapper.editedReqSession(s, {"remove": ["Authorization", "X-Fingerprint"]})

	def getXFingerprint(self, generateIfNone):
		url = self.discord + "experiments"
		headerMods = {"update":{"X-Context-Properties":ContextProperties.get("/app")}}
		reqxfinger = Wrapper.sendRequest(self.editedS, 'get', url, headerModifications=headerMods, log=self.log)
		if generateIfNone and not reqxfinger:
			snowflake = calculateNonce()
			randomPart = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(27))
			xfingerprint = '{}.{}'.format(snowflake, randomPart)
		else:
			xfingerprint = reqxfinger.json().get('fingerprint')
		return xfingerprint

	def login(self, email, password, undelete, captcha, source, gift_code_sku_id, secret, code):
		url = self.discord + "auth/login"
		self.xfingerprint = self.getXFingerprint(True)
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

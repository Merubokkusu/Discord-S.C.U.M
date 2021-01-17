from ..RESTapiwrap import *

class Stickers(object):
	def __init__(self, discord, s, log): #s is the requests session object
		self.discord = discord
		self.s = s
		self.log = log

	def getStickers(self, directoryID="758482250722574376", store_listings=False, locale="en-US"):
		store_listings = str(store_listings).lower()
		url = self.discord+"sticker-packs/directory-v2/"+directoryID+"?with_store_listings="+store_listings+"&locale="+locale
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	def getStickerFile(self, stickerID, stickerAsset): #this is an apng
		url = "https://media.discordapp.net/stickers/"+stickerID+"/"+stickerAsset+".png"
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	def getStickerJson(self, stickerID, stickerAsset):
		url = "https://discord.com/stickers/"+stickerID+"/"+stickerAsset+".json"
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	def getStickerPack(self, stickerPackID):
		url = self.discord+"sticker-packs/"+stickerPackID
		return Wrapper.sendRequest(self.s, 'get', url, log=self.log)

	
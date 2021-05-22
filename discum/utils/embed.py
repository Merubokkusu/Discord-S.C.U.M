class Embedder(object):
    def __init__(self):
        self.jsonEmbed = {"fields": []} #Create a 'fields' key otherwise we can't add anything to it, plus it doesn't effect anything if nothing is added.

    def read(self):
        return self.jsonEmbed

    def title(self,title):
        self.jsonEmbed.update({'title': title}) 

    def description(self,description):
        self.jsonEmbed.update({'description': description}) 

    def url(self,url):
        self.jsonEmbed.update({'url': url}) 

    def color(self,color):
        self.jsonEmbed.update({'color': color}) 

    def footer(self,text,iconURL=""):
        self.jsonEmbed.update({'footer': {
            'icon_url': iconURL,
            'text': text
        }}) 

    def image(self,url):
        self.jsonEmbed.update({'image': {
            'url': url,
        }})

    def thumbnail(self,url):
        self.jsonEmbed.update({'thumbnail': {
            'url': url,
        }})

    def author(self,name,url="",icon_url=""):
        self.jsonEmbed.update({'author': {
            'name': name,
            'url': url,
            'icon_url':icon_url
        }})

    def fields(self,name,value,inline=False):
        self.jsonEmbed['fields'].append({
            'name': name,
            'value': value,
            'inline': inline
        })
    
    
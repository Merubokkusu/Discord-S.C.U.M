'''
DISCUM: A SELFBOT DISCORD API. 
developed by Merubokkusu and arandomnewaccount
does not use any premade discord libraries, made to be simple (sorta) and expandable
'''
import requests,json

from .messages.messages import Messages
from .messages.embed import Embedder
from .user.user import User

class LoginError(Exception):
    pass

class Client(object):
    # Define token, headers and create the request session.
    def __init__(self,email,password): # if you'd like to input your token instead, change this line to def __init__(self,token): and replace lines 18-26 with self.token = token
        self.email = email
        self.password = password
        self.discord = 'https://discord.com/api/v6/'
        logindata = json.dumps({'email': self.email, 'password':self.password}).encode('utf-8')
        req = requests.post(self.discord+'/auth/login', data=logindata, headers={'Content-Type':'application/json'})
        if req.status_code == 200:
            self.token = req.json()['token']
            print('Connected.')
        else:
            raise LoginError("Incorrect email and/or password.")
        self.headers = {
        "Host": "discord.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.306 Chrome/78.0.3904.130 Electron/7.1.11 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "en-US",
        "Accept-Encoding": "gzip, deflate, br",
        "Authorization": self.token,
        "Connection": "keep-alive",
        "keep-alive" : "timeout=10, max=1000",
        "TE": "Trailers",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Referer": "https://discord.com/channels/@me",
        "Content-Type": "application/json"
        }
        self.s = requests.Session()
        self.s.headers.update(self.headers)
        
    #test token
    def connectionTest(self): #,proxy):
        url=self.discord+'users/@me/affinities/users'
        connection = self.s.get(url)
        if(connection.status_code == 200):
            print("Connected")
        else:
            print("Incorrect Token")

    '''
    Messages
    '''
    #get messages
    def getMessage(self,channelID,num=1):
        return Messages(self.discord,self.headers).getMessage(channelID,num)

    #send text or embed messages
    def sendMessage(self,channelID,message,embed="",tts=False):
        return Messages(self.discord,self.headers).sendMessage(channelID,message,embed,tts)

    #send files (local or link)
    def sendFile(self,channelID,filelocation,isurl=False,message=""):
        return Messages(self.discord,self.headers).sendFile(channelID,filelocation,isurl,message)

    '''
    User
    '''
    #get list of DMs (to get Messages use getMessage function above with the DM id)
    def getDMs(self):
        return User(self.discord,self.headers).getDMs()

    #get list of guilds
    def getGuilds(self):
        return User(self.discord,self.headers).getGuilds()

    #get relationships info (1=friend, 2=block, 3=incoming friend request, 4=outgoing friend request)
    def getRelationships(self):
        return User(self.discord,self.headers).getRelationships()

    #create outgoing friend request
    def requestFriend(self,ID):
        return User(self.discord,self.headers).requestFriend(ID)

    #accept incoming friend request
    def acceptFriend(self,ID):
        return User(self.discord,self.headers).acceptFriend(ID)

    #remove friend OR unblock user
    def removeRelationship(self,ID):
        return User(self.discord,self.headers).removeRelationship(ID)

    #block user
    def blockUser(self,ID):
        return User(self.discord,self.headers).blockUser(ID)

    def changeName(self,name):
        return User(self.discord,self.headers).changeName(self.email,self.password,name)
    
    def setStatus(self,status):
        return User(self.discord,self.headers).setStatus(status)
    
    def setAvatar(self,imagePath):
        return User(self.discord,self.headers).setAvatar(self.email,self.password,imagePath)

#influence for much of this code came from here: https://github.com/Gehock/discord-ws
import asyncio
import websockets
import json
from collections import Counter

class TaskCompleted(Exception):
    pass

class GatewayServer():

    class LogLevel:
        SEND = '\033[94m'
        RECEIVE = '\033[92m'
        WARNING = '\033[93m'
        DEFAULT = '\033[m'

    class OPCODE: #https://discordapp.com/developers/docs/topics/opcodes-and-status-codes
        # Name                  Code    Client Action   Description
        DISPATCH =              0  #    Receive         dispatches an event
        HEARTBEAT =             1  #    Send/Receive    used for ping checking
        IDENTIFY =              2  #    Send            used for client handshake
        STATUS_UPDATE =         3  #    Send            used to update the client status
        VOICE_UPDATE =          4  #    Send            used to join/move/leave voice channels
        #                       5  #    ???             ???
        RESUME =                6  #    Send            used to resume a closed connection
        RECONNECT =             7  #    Receive         used to tell clients to reconnect to the gateway
        REQUEST_GUILD_MEMBERS = 8  #    Send            used to request guild members
        INVALID_SESSION =       9  #    Receive         used to notify client they have an invalid session id
        HELLO =                 10 #    Receive         sent immediately after connecting, contains heartbeat and server debug information
        HEARTBEAT_ACK =         11 #    Sent immediately following a client heartbeat that was received
        GUILD_SYNC =            12 #    ???             ???

    def __init__(self, websocketurl, token, ua_data, proxy_host, proxy_port, log):
        self.log = log
        self.websocketurl = websocketurl
        self.token = token
        self.ua_data = ua_data
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.interval = None
        self.sequence = None

        self.session_id = None
        self.session_data = None
        self.session_settings_gathered = False #before, we could simply check if the session settings had stuff in it. Now that session settings arrives in 2 parts, this is no longer the ideal way to check whether or not session settings has been fully gathered.

        self.all_tasks = {} #just the task input. all of it
        self.receiveData = [] #the receive value input
        self.results = [] #output

        #as far as checklists go, allTasks variables have values looking like None or "complete" which subtasks have values looking like [None] or ["complete"]. The exception is in the mailSent subtask, which has a value of either True or False.
        self.receiveChecklist = [] #acts as a checklist for receive, looks at the current task
        self.mailSent = False #just checks whether or not data has finished sending, looks at the current task
        self.allTasksChecklist = {} #checklist for all tasks

        self.taskCompleted = False #is current task completed?
        self.allTasksCompleted = False #are all tasks completed?, technically unnecessary, but it's here in case youre confused about how the code works
        #self.taskCompleteConstant = {}


        self.auth = {
                "token": self.token,
                "capabilities": 61,
                "properties": {
                    "os": self.ua_data["os"],
                    "browser": self.ua_data["browser"],
                    "device": self.ua_data["device"],
                    "browser_user_agent": self.ua_data["browser_user_agent"],
                    "browser_version": self.ua_data["browser_version"],
                    "os_version": self.ua_data["os_version"],
                    "referrer": "",
                    "referring_domain": "",
                    "referrer_current": "",
                    "referring_domain_current": "",
                    "release_channel": "stable",
                    "client_build_number": 70781,
                    "client_event_source": None
                },
                "presence": {
                    "status": "online",
                    "since": 0,
                    "activities": [],
                    "afk": False
                },
                "compress": False,
                "client_state": {
                    "guild_hashes": {},
                    "highest_last_message_id": "0",
                    "read_state_version": 0,
                    "user_guild_settings_version": -1
                }
            }
        if 'build_num' in self.ua_data and self.ua_data['build_num']!=70781:
            self.auth['properties']['client_build_number'] = self.ua_data['build_num']

        self.loop = asyncio.get_event_loop()

        #variables for calling
        self.channelID = None
        self.userID = None
        self.media_token = None
        self.call_endpoint = None
        self.call_session_id = None


    def key_checker(self, element, keys):
        _element = element
        for key in keys:
            try:
                _element = _element[key]
            except (KeyError, TypeError) as e:
                return False
        return True

    def value_checker(self, element, keys, valuetest):
        _element = element
        for index,key in enumerate(keys):
            try:
                _element = _element[key]
                if index==len(keys)-1 and _element != valuetest:
                   return False
            except (KeyError, TypeError) as e:
                return False
        return True

    def NestedDictValues(self,d): #gets all values of a nested dict
        for v in d.values():
            if isinstance(v, dict):
                yield from self.NestedDictValues(v)
            else:
                yield v

    def run(self,tasks,log):
        self.log = log #update log
        self.results = [] #clear results list
        self.session_data = None #reset
        self.session_settings_gathered = False #reset
        self.all_tasks = tasks
        if self.all_tasks != 'get session data':
            self.allTasksChecklist = {key: None for key in self.all_tasks.keys()} #looks like {1:None,2:None,etc}
        else:
        	self.allTasksChecklist = {1:'get session data'}
        try:
            asyncio.run(self.main())
        except TaskCompleted:
            self.loop.stop()
            return self.results #yay

    async def taskManager(self):
        if self.all_tasks != 'get session data':
            self.taskCompleted = True #necessary for first task to begin
            for index in self.all_tasks:
                if self.log: print('task num: '+str(index))
                while not self.session_settings_gathered: #wait till ready supplemental is received
                    await asyncio.sleep(0)
                await self.addTask(self.all_tasks[index])
                while self.taskCompleted == False: #this just waits till task is completed
                    await asyncio.sleep(0)
                self.taskCompleted = False #reset
                self.allTasksChecklist[index] = "complete"
                if self.log: print(self.allTasksChecklist)
        else:
            while not self.session_settings_gathered:
                await asyncio.sleep(0)
            self.allTasksChecklist[1] = "complete" #the index might seem wrong, but remember that the format of this dict is {1:value,2:value,etc}

    async def main(self): # http_proxy_host=self.proxy_host, http_proxy_port=self.proxy_port
        if self.proxy_host == None:
            async with websockets.connect(
                    self.websocketurl, origin="https://discordapp.com") \
                    as self.websocket:
                if self.log: print("Connected to "+self.websocketurl)
                await self.hello()
                if self.interval is None:
                    if self.log: print(self.LogLevel.WARNING + "Hello failed, exiting")
                    if self.log: print(self.LogLevel.DEFAULT)
                    return
                await asyncio.gather(self.heartbeat(), self.receive(),self.stopLoop(),self.taskManager())
        else:
            async with websockets.connect(
                    self.websocketurl, origin="https://discordapp.com", host=self.proxy_host, port=self.proxy_port) \
                    as self.websocket:
                if self.log: print("Connected to "+self.websocketurl)
                await self.hello()
                if self.interval is None:
                    if self.log: print(self.LogLevel.WARNING + "Hello failed, exiting")
                    if self.log: print(self.LogLevel.DEFAULT)
                    return
                await asyncio.gather(self.heartbeat(), self.receive(),self.stopLoop(),self.taskManager())

    async def receive(self):
        if self.log: print("Entering receive")
        async for message in self.websocket:
            if self.log: print(self.LogLevel.RECEIVE + "<", message)
            if self.log: print(self.LogLevel.DEFAULT)
            data = json.loads(message)
            #the following lines are technically optional if youre using GatewayServer separately, I simply have them here for convenience
            if data["op"] == self.OPCODE.DISPATCH:
                self.sequence = int(data["s"]) #necessary
                event_type = data["t"]
                if event_type == "READY":
                    self.session_id = data["d"]["session_id"]
                    self.session_data = data
                if event_type == "READY_SUPPLEMENTAL":
                    self.session_data['d'].update(data['d']) #cause it's easier to parse both READY and READY_SUPPLEMENTAL this way
                    self.session_settings_gathered = True
                if event_type == "VOICE_SERVER_UPDATE":
                    if "token" in data["d"]:
                        self.media_token = data["d"]["token"]
                    if "endpoint" in data["d"]:
                        endpointdata = data["d"]["endpoint"].split(':')[:][0]
                        self.call_endpoint = "wss://{}/?v=5".format(endpointdata)
                if event_type == "VOICE_STATE_UPDATE":
                    if "user_id" in data["d"]:
                        self.userID = data["d"]["user_id"]
                    if "session_id" in data["d"]:
                        self.call_session_id = data["d"]["session_id"]
            #onto updating self.receiveChecklist
            for checklistIndex in range(len(self.receiveChecklist)): #for each message, every receive is checked just in case
                if self.receiveChecklist[checklistIndex] != ["complete"]:
                    if "key" in self.receiveChecklist[checklistIndex] and all([self.key_checker(data,i) for i in self.receiveData[checklistIndex]["key"]]): #just looping thru the tuples
                        self.receiveChecklist[checklistIndex]["key"] = ["complete"]
                    if "keyvalue" in self.receiveChecklist[checklistIndex] and all([self.value_checker(data,i[0],i[1]) for i in self.receiveData[checklistIndex]["keyvalue"]]): #just looping thru the tuples
                        self.receiveChecklist[checklistIndex]["keyvalue"] = ["complete"]
                    if all(value == ["complete"] for value in list(self.NestedDictValues(self.receiveChecklist[checklistIndex]))): # and self.mailSent check mail sent later...
                        self.receiveChecklist[checklistIndex] = ["complete"]
                        self.results.append(data)
                        break #after first match is found, break
            if len(self.receiveChecklist)>0 and all(item == ["complete"] for item in self.receiveChecklist) and self.mailSent:
                self.taskCompleted = True #current task is completed

    async def send(self, opcode, payload):
        data = self.opcode(opcode, payload)
        if self.log: print(self.LogLevel.SEND + ">", data)
        if self.log: print(self.LogLevel.DEFAULT)
        await self.websocket.send(data)

    async def heartbeat(self):
        if self.log: print("Entering heartbeat")
        while self.interval is not None:
            if self.log: print("Sending a heartbeat")
            await self.send(self.OPCODE.HEARTBEAT, self.sequence)
            await asyncio.sleep(self.interval)

    async def hello(self):
        await self.send(self.OPCODE.IDENTIFY, self.auth)
        if self.log: print(self.LogLevel.SEND + "hello > auth")
        if self.log: print(self.LogLevel.DEFAULT)

        ret = await self.websocket.recv()
        if self.log: print("{}hello < {}".format(self.LogLevel.RECEIVE,ret))
        if self.log: print(self.LogLevel.DEFAULT)

        data = json.loads(ret)
        opcode = data["op"]
        if opcode != 10:
            if self.log: print(self.LogLevel.WARNING + "Unexpected reply")
            if self.log: print(ret)
            if self.log: print(self.LogLevel.DEFAULT)
            return
        self.interval = (data["d"]["heartbeat_interval"] - 2000) / 1000
        if self.log: print("interval:", self.interval)

    def opcode(self, opcode: int, payload) -> str:
        data = {
            "op": opcode,
            "d": payload
        }
        return json.dumps(data)

    async def addTask(self,data):
        self.mailSent = False #reset
        self.taskCompleted = False #reset
        self.receiveChecklist = [] #reset
        self.receiveData = data["receive"]
        for searchIndex in range(len(self.receiveData)):
            self.receiveChecklist.append({})
            if "key" in self.receiveData[searchIndex]:
                self.receiveChecklist[searchIndex]["key"] = [None]
            if "keyvalue" in self.receiveData[searchIndex]:
                self.receiveChecklist[searchIndex]["keyvalue"] = [None]
        sendData = data["send"] #have to also check if all data has been sent.............
        for mail in sendData: #send data if theres data to send
            #if you want to make changes to mail make that here
            await self.send(mail["op"],mail["d"])
        self.mailSent = True

    async def stopLoop(self):
        while not all(value == "complete" for value in self.allTasksChecklist.values()):
            await asyncio.sleep(0)
        self.allTasksCompleted = True
        raise TaskCompleted(self.all_tasks)

'''
# although calling is not supported yet on discum, you can still initial calls with this program (and send data if you get creative). below lies an example code for calling another user (just input your token and the channel id)
if __name__ == "__main__":
    gateway = GatewayServer(your_token_here,None,None,True)
    gateway.run(taskdata, log) #loop stops a few seconds after allTasksCompleted == True
    #gateway.run('get session data', log=True)
    #gateway.run({1:{"send":[],"receive":[]}}, log=True)
'''

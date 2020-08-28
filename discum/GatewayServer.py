#influence for much of this code came from here: https://github.com/Gehock/discord-ws
import asyncio
import websockets
import json

class TaskCompleted(Exception):
    pass

class GatewayServer():

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

    def __init__(self, token, proxy_host, proxy_port):
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.interval = None
        self.sequence = None
        self.session_id = None
        self.session_data = None
        self.checkit = {} #see receive function
        self.task_data = []
        self.taskCompleted = False
        self.mainTaskCompleted = False
        self.taskCompleteConstant = {}
        self.stopIt = False
        self.taskComplete = {}
        self.mainTaskComplete = {}
        self.all_tasks = {}

        self.auth = {
                "token": token,
                "properties": {
                    "os": "Windows",
                    "browser": "Chrome",
                    "device": "",
                },
                "large_threshold": 150,
                "synced_guilds": [],
                "presence": {
                    "status": "online",
                    "since": 0,
                    "afk": False,
                    "game": None
                },
                "compress": False
            }

        self.loop = asyncio.get_event_loop()

        #variables for calling
        self.channelID = None
        self.userID = None
        self.media_token = None
        self.call_endpoint = None
        self.call_session_id = None


    def NestedDictValues(self,d):
        for v in d.values():
            if isinstance(v, dict):
                yield from self.NestedDictValues(v)
            else:
                yield v

    def runIt(self,tasks):
        self.all_tasks = tasks
        if self.all_tasks != 'get session data':
            self.mainTaskComplete = {key: None for key in self.all_tasks.keys()}
        else:
        	self.mainTaskComplete = {1:'get session data'}

        try:
            asyncio.run(self.main())
        except TaskCompleted:
            self.loop.stop()

    async def taskManager(self):
        if self.all_tasks != 'get session data':
            for index in self.all_tasks:
                print('task num: '+str(index))
                await self.addTask(self.all_tasks[index])
                while self.mainTaskCompleted == False:
                    await asyncio.sleep(1)
                self.mainTaskCompleted = True #reset mainTaskCompleted
                self.mainTaskComplete[index] = "complete"
        else:
            while self.session_data is None:
                await asyncio.sleep(1)
            self.mainTaskComplete[1] = 'complete'

    async def main(self): # http_proxy_host=self.proxy_host, http_proxy_port=self.proxy_port
        if self.proxy_host == None:
            async with websockets.connect(
                    'wss://gateway.discord.gg/?v=6&encoding=json', origin="https://discordapp.com") \
                    as self.websocket:
                await self.hello()
                if self.interval is None:
                    print("Hello failed, exiting")
                    return
                await asyncio.gather(self.heartbeat(), self.receive(),self.stopLoop(),self.taskManager())
        else:
            async with websockets.connect(
                    'wss://gateway.discord.gg/?v=6&encoding=json', origin="https://discordapp.com", host=self.proxy_host, port=self.proxy_port) \
                    as self.websocket:
                await self.hello()
                if self.interval is None:
                    print("Hello failed, exiting")
                    return
                await asyncio.gather(self.heartbeat(), self.receive(),self.stopLoop(),self.taskManager())

    async def receive(self):
        print("Entering receive")
        async for message in self.websocket:
            self.taskComplete = self.taskCompleteConstant
            print("<", message)
            #print("Recieved message from server.")
            data = json.loads(message)
            if data["op"] == self.OPCODE.DISPATCH:
                self.sequence = int(data["s"])
                event_type = data["t"]
                if event_type == "READY":
                    self.session_id = data["d"]["session_id"]
                    self.session_data = data
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
            if "op" in self.taskComplete and self.task["op"] == data["op"]:
                self.taskComplete["op"] = "complete"
            if "d" in self.taskComplete:
                if "key" in self.taskComplete["d"] and self.task["d"]["key"] in data["d"]:
                    self.taskComplete["d"]["key"] = "complete"
                if "value" in self.taskComplete["d"] and self.task["d"]["value"] in data["d"].values():
                    self.taskComplete["d"]["value"] = "complete"
                if "text" in self.taskComplete["d"] and self.task["d"]["text"] in str(data["d"]):
                    self.taskComplete["d"]["text"] = "complete"
            if "s" in self.taskComplete and self.task["s"] == data["s"]:
                self.taskComplete["s"] = "complete"
            if "t" in self.taskComplete and self.task["t"] == data["t"]:
                self.taskComplete["t"] = "complete"
            if "count" in self.taskComplete and "complete" in list(self.taskComplete.values()):
                self.current_count+=1
                if self.current_count == self.task["count"]:
                    self.taskComplete["count"] = "complete"
            if all(value == "complete" for value in list(self.NestedDictValues(self.taskComplete))):
                self.current_count = 0 #reset count
                self.task_data.append(data) #this is only accurate for checking len(self.task_data). the data itself can be inaccurate if there are multiple simultaneous responses
                print(self.task_data)
                self.taskCompleted = True 
                if len(self.task_data) == len(self.checkit):
                    self.mainTaskCompleted = True

    async def send(self, opcode, payload):
        data = self.opcode(opcode, payload)
        print(">", data)
        await self.websocket.send(data)

    async def heartbeat(self):
        print("Entering heartbeat")
        while self.interval is not None:
            print("Sending a heartbeat")
            await self.send(self.OPCODE.HEARTBEAT, self.sequence)
            await asyncio.sleep(self.interval)

    async def hello(self):
        await self.send(self.OPCODE.IDENTIFY, self.auth)
        print(f"hello > auth")

        ret = await self.websocket.recv()
        print(f"hello < {ret}")

        data = json.loads(ret)
        opcode = data["op"]
        if opcode != 10:
            print("Unexpected reply")
            print(ret)
            return
        self.interval = (data["d"]["heartbeat_interval"] - 2000) / 1000
        print("interval:", self.interval)

    def opcode(self, opcode: int, payload) -> str:
        data = {
            "op": opcode,
            "d": payload
        }
        return json.dumps(data)

    async def addTask(self,data):
        while self.taskCompleted == False:
            await asyncio.sleep(1)
        self.taskCompleted = False #reset
        sendData = data["send"]
        for mail in sendData: #send data if theres data to send
            #if you want to make changes to mail make that here
            await self.send(mail["op"],mail["d"])
        receiveData = data["receive"]
        self.checkit = receiveData
        self.task_data = [] #clear it
        for search in receiveData: #receive data is essentially a search function (look at async def receive)
            self.taskCompleted = False
            #task processing
            self.task = search
            self.keylist = self.task.keys()
            self.taskComplete = {}
            self.current_count = 0
            if "op" in self.task:
                self.taskComplete["op"] = None
            if "d" in self.task:
                self.taskComplete["d"] = {}
                if "key" in self.task["d"]:
                    self.taskComplete["d"]["key"] = None
                if "value" in self.task["d"]:
                    self.taskComplete["d"]["value"] = None
                if "text" in self.task["d"]:
                    self.taskComplete["d"]["text"] = None
            if "s" in self.task:
                self.taskComplete["s"] = None
            if "t" in self.task:
                self.taskComplete["t"] = None
            if "count" in self.task:
                self.taskComplete["count"] = None
            self.taskCompleteConstant = self.taskComplete

    async def stopLoop(self):
        while not all(value == "complete" for value in self.mainTaskComplete.values()):
            await asyncio.sleep(1)
        raise TaskCompleted(self.all_tasks)

# although calling is not supported yet on discum, you can still initial calls with this program (and send data if you get creative). below lies an example code for calling another user (just input your token and the channel id)
'''
if __name__ == "__main__":
    gateway = GatewayServer(your_token_here,None,None)
    gateway.runIt({1:{"send":[{"op":4,"d":{"guild_id":None,"channel_id":CHANNEL_ID_HERE,"self_mute":False,"self_deaf":False,"self_video":False}}],"receive":[{"t":"VOICE_SERVER_UPDATE"}]}})
'''

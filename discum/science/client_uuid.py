import math, random
import time, datetime
import struct
import base64

class Client_UUID(object): #Huge thanks to github user fweak for helping me figure out the mystery of the client_uuid. made some discord "science" notes here: https://docs.google.com/document/d/1b5aDx7S1iLHoeb6B56izZakbXItA84gUjFzK-0OBwy0
    def __init__(self, userID, creationTime="now", eventNum=0):
        self.userID = int(userID)
        num = int(4294967296 * random.random())
        self.randomPrefix = num if num<=2147483647 else num-4294967296
        self.creationTime = int(time.mktime(datetime.datetime.now().timetuple()) * 1000) if creationTime == "now" else creationTime
        self.eventNum = eventNum
        self.UUID = ""

    def calculate(self, eventNum="default", userID="default", increment=True):
        if eventNum == "default":
            eventNum = self.eventNum
        if userID == "default":
            userID = self.userID
        else:
            userID = int(userID)

        buf = bytearray(struct.pack('24x'))
        buf[0:4] = bytes(struct.pack("<i", userID%4294967296 if userID%4294967296<=2147483647 else userID%4294967296-2147483647))
        buf[4:8] = bytes(struct.pack("<i", userID>>32))
        buf[8:12] = bytes(struct.pack("<i", self.randomPrefix))
        buf[12:14] = bytes(struct.pack("<i", self.creationTime%4294967296 if self.creationTime%4294967296<=2147483647 else self.creationTime%4294967296-2147483647))
        buf[16:20] = bytes(struct.pack("<i", self.creationTime>>32))
        buf[20:24] = bytes(struct.pack("<i", eventNum))

        if increment:
            self.eventNum += 1
        self.UUID = base64.b64encode(buf).decode('ascii')
        return self.UUID

    def refresh(self, resetEventNum=True):
        self.randomPrefix = num if num<=2147483647 else num-4294967296
        self.creationTime = int(time.mktime(datetime.datetime.now().timetuple()) * 1000) if creationTime == "now" else creationTime
        if resetEventNum:
            self.eventNum = 0
        return self.calculate()

    @staticmethod
    def parse(client_uuid): #need to correct userID calculation*
        parts = []
        for i in range(int(len(base64.b64decode(client_uuid))/4)):
            parts.append(struct.unpack('<i', base64.b64decode(client_uuid)[4*i:4*i+4])[0])
        userID = str(parts[1]<<32)
        randomPrefix = parts[2]
        creationTime = parts[4]<<32
        eventNum = parts[5]
        return {'userID':userID, 'randomPrefix':randomPrefix, 'creationTime':creationTime, 'eventNum':eventNum}

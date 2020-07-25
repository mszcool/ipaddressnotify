#
# Encapsulates sending and receiving messages with IP address updates to/from a queue
#

import json
from datetime import datetime
from azure.storage.queue import QueueService

QUEUE_NAME = "ipaddressqueue"

class IPMessage:

    def __init__(self):
        self.currentdate = datetime.now()
        self.ipaddress = "0.0.0.0"

    @property
    def currentDate(self):
        return self.currentdate

    @property
    def ipAddress(self):
        return self.ipaddress

    def getJsonMessage(self):
        data = {}
        data["ipAddress"] = self.ipaddress
        data["changeDate"] = self.currentdate.strftime("%Y-%m-%d")
        data["changeTime"] = self.currentdate.strftime("%H:%M:%S")
        json.loads(data)
        return(str(json))
    
    def loadJsonMessage(self, data):
        json.loads(data)
        self.ipaddress = data["ipAddress"]
        dateData = str.split(data["changeDate"], '-')
        timeData = str.split(data["changeTime"], ':')
        # Note - this requires validation, will do so once I've tested the flow
        self.currentdate = datetime(dateData[0], dateData[1], dateData[2], timeData[0], timeData[1], timeData[2])
        
class IPMessageTransmitter:

    def __init__(self, queueConnectionString):
        self.connectionString = queueConnectionString

    def processMessage(self, ipAdr, action):
        queueService = QueueService(connection_string=self.connectionString)
        if queueService.exists(QUEUE_NAME) == False:
            return
        messages = queueService.get_messages(QUEUE_NAME)
        try:
            for m in messages:
                ipData = IPMessage()
                ipData.loadJsonMessage(m.content)
                action(ipData)
                queueService.delete_message(QUEUE_NAME, m.id, m.pop_receipt)
        except:
            raise Exception("failed processing message") 

        return messages

    def sendMessage(self, ipAdr):
        queueService = QueueService(connection_string=self.connectionString)
        if queueService.exists(QUEUE_NAME) == False:
            queueService.create_queue(QUEUE_NAME)
        queueService.put_message(QUEUE_NAME, ipAdr.getJsonMessage())
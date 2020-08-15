#
# Encapsulates sending and receiving messages with IP address updates to/from a queue
#

import json
from datetime import datetime
from azure.storage.queue import QueueClient
from azure.storage.queue import QueueServiceClient

QUEUE_NAME = u"ipaddressqueue"

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
        jsonStr = json.dumps(data)
        return(jsonStr)
    
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
        self.queueSvc = QueueServiceClient.from_connection_string(conn_str=self.connectionString, queue_name=QUEUE_NAME) 

    def existsQueue(self):
        foundQ = False
        queuesList = self.queueSvc.list_queues()
        for queue in queuesList:
            if(queue.name == QUEUE_NAME):
                foundQ = True
                break
        return foundQ

    def processMessage(self, action):
        # If no queue exists, cancel the operation and return False to indicate now messages are available
        if not self.existsQueue():
            return 0

        # Get the queue and get some messages (if it exists)
        messagesProcessed = 0
        queue = self.queueSvc.get_queue_client(QUEUE_NAME)
        messages = queue.receive_messages(messages_per_page=5)
        queue.get_queue_properties()
        try:
            for m in messages.by_page():
                if m.dequeue_count > 3:
                    queue.delete_message(m)
                else:
                    ipData = IPMessage()
                    ipData.loadJsonMessage(m.content)
                    action(ipData)
                    queue.delete_message(m)
                    messagesProcessed += 1
        except:
            raise Exception("failed processing message") 

        return messagesProcessed

    def sendMessage(self, ipAdr):
        # Create the queue if it does not exist
        if not self.existsQueue():
            try:
                self.queueSvc.create_queue(QUEUE_NAME)
            except:
                raise Exception("Failed creating queue %s" % QUEUE_NAME)

        # Prepare the IP address message
        ipData = IPMessage()
        ipData.currentdate = datetime.now()
        ipData.ipaddress = ipAdr
        queue = self.queueSvc.get_queue_client(QUEUE_NAME)
        queue.send_message(ipData.getJsonMessage())        
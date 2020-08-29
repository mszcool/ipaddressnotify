#
# Main program - gets OS' current IP address and sends a message or gets the message from the queue depending on command line parameter
#

import os
import sys

import urllib
from ipmessageprocessing import IPMessage
from ipmessageprocessing import IPMessageTransmitter

#
# A few global parameters
#
MESSAGE_RETRIEVE_COUNT=1
ENV_CONNSTR_NAME="queueConnStr"
IPADDRESSRESOLVER_URL_PRI="https://api.ipify.org/?format=text"
IPADDRESSRESOLVER_URL_SEC="http://ipv4bot.whatismyipaddress.com/"

#
# Prints out a help
#
def printHelp():
    print("IP Address Resolver Tool for Remote locations!")
    print("ipnotifyer.py read\tReads if there is a change from an Azure Queue")
    print("ipnotifyer.py write\tWrites the current public IP address to the Azure Queue")
    print("ipnotifyer.py dump\tDumps the current IP Address on the console without doing anything")

#
# Reads the current public IP address through two alternative sources
#
def getCurrentIpAddress():
    try: 
        webReq = urllib.request.urlopen(IPADDRESSRESOLVER_URL_PRI)
    except:
        try:
            webReq = urllib.request.urlopen(IPADDRESSRESOLVER_URL_SEC)
        except:
            return ""
    if webReq.getcode() == 200:
        # Return the IP address
        data = webReq.read().decode("utf-8")
        return str(data)
    else:
        return ""

#
# Post things to the Azure Queue
#
def postIPAddress():
    # Reading the connection string from the environment
    connStr = os.environ[ENV_CONNSTR_NAME]
    ipAdr = getCurrentIpAddress()
    queuePoster = IPMessageTransmitter(connStr)
    queuePoster.sendMessage(ipAdr)
    print ("{ \"ipQueued\": \"%s\" }" % ipAdr)

#
# Get things from the Azure Queue
#
def getIPAddressMessages():
    connStr = os.environ[ENV_CONNSTR_NAME]
    queueReader = IPMessageTransmitter(connStr)
    queueReader.processMessage(MESSAGE_RETRIEVE_COUNT, ipAddressAction)

#
# The application itself just dumps the IP address object onto the console
#
def ipAddressAction(ipData: IPMessage):
    print(ipData.getJsonMessage())


#
# Main program logic
#
def main():
    # Parse the command line values
    argValues = sys.argv
    if(argValues.__len__() != 2):
        printHelp()
    if argValues[1] == "read":
        getIPAddressMessages()
    elif argValues[1] == "write":
        postIPAddress()
    elif argValues[1] == "dump":
        ipAdr = getCurrentIpAddress()
        print(ipAdr)
    else:
        print("<< Unknown argument %s >>" % argValues[0])
        printHelp()

if __name__ == "__main__":
    main()
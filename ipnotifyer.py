#
# Main program - gets OS' current IP address and sends a message or gets the message from the queue depending on command line parameter
#

import os
import sys

import urllib
from ipmessageprocessing import IPMessage
from ipmessageprocessing import IPMessageTransmitter

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
def postIpAddress():
    # Reading the connection string from the environment
    connStr = os.environ['queueConnStr']
    ipAdr = getCurrentIpAddress()
    queuePoster = IPMessageTransmitter(connStr)
    queuePoster.sendMessage(ipAdr)
    print ("Sent message with current IP %s" % ipAdr)

#
# Get things from the Azure Queue
#
def getIpAddressMessages():
    print ("Hey")

#
# Main program logic
#
def main():
    # Parse the command line values
    argValues = sys.argv
    if(argValues.__len__() != 2):
        printHelp()
    if argValues[1] == "read":
        print("Getting stuff from Azure Queue")
    elif argValues[1] == "write":
        postIpAddress()
    elif argValues[1] == "dump":
        ipAdr = getCurrentIpAddress()
        print(ipAdr)
    else:
        print("<< Unknown argument %s >>" % argValues[0])
        printHelp()

if __name__ == "__main__":
    main()
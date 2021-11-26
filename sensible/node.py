import threading
from time import sleep

from sensible.client import runClient 
from sensible.server import runServer 
from sensible.sensors import runSensors
from sensible.interactive_interface import getInterface

def createVariables():
    lock = threading.Lock()
    data = {}
    otherData = {}
    
    clientLog = []
    serverLog = []
    return (lock, data, otherData, clientLog, serverLog)

def runNode(port):
    (lock, data, otherData, clientLog, serverLog) = createVariables()
    runSensors(lock, data)
    runClient(lock, otherData, clientLog)
    runServer(lock, data, serverLog, port)
    return getInterface(lock, data, otherData, clientLog, serverLog, port)
    
    # while True:
    #     print("serverLog:", serverLog)
    #     print("clientLog:", clientLog)

    #     print("requestedData:", otherData)
    #     sleep(2)

import threading
from time import sleep

from sensible.client import runClient 
from sensible.server import runServer 
from sensible.sensors import runSensors 

def createVariables():
    lock = threading.Lock()
    data = {}
    otherData = {}
    
    clientLog = []
    serverLog = []
    return (lock, data, otherData, clientLog, serverLog)

def runNode() -> None:
    (lock, data, otherData, clientLog, serverLog) = createVariables()
    runSensors(lock, data)
    runClient(lock, otherData, clientLog)
    runServer(lock, data, serverLog)
    while True:
        print("serverLog:", serverLog)
        print("clientLog:", clientLog)
        sleep(2)

import threading
from time import sleep

from sensible.client import runClient 
from sensible.server import runServer 
from sensible.sensors import runSensors

def createVariables():
    state = {"lock": threading.Lock(),
             "data": {},
             "otherData": {},
             "clientLog": [],
             "serverLog": [],}
    return state

def createConfig(port, addresses, sensorType):
    config = {"port": port,
              "addresses": addresses,
              "sensorType": sensorType}
    return config

def runNode(config):
    state = createVariables()
    runSensors(**state, **config)
    runClient(**state, **config)
    runServer(**state, **config)
    return state

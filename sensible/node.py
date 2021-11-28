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

def createConfig(port, addresses, sensor_procedures):
    config = {"port": port,
              "addresses": addresses,
              "sensor_procedures": sensor_procedures}
    # A sensor procedure is a function takes in two arguments
    # the thread lock,
    # and a data array to append sensor values to 
    return config

def runNode(config):
    state = createVariables()
    runSensors(**state, **config)
    runClient(**state, **config)
    runServer(**state, **config)
    return state

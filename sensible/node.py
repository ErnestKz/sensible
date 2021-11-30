import threading
from time import sleep

from sensible.client import runClient 
from sensible.server import runServer 
from sensible.sensors import runSensors
from sensible.database import createDatabase

def createVariables():
    state = {"lock": threading.Lock(),
             "data": {},
             "otherData": {},
             "clientLog": [],
             "serverLog": [],}
    return state

def createConfig(port, deviceAddress, addresses, sensor_procedures):
    config = {"port": port,
              "deviceAddress": deviceAddress,
              "addresses": addresses,
              "sensor_procedures": sensor_procedures}
    # A sensor procedure is a function takes in two arguments
    # the thread lock,
    # and a data array to append sensor values to 
    return config

def runNode(config):
    state = createVariables()
    createDatabase(**state, **config)
    runSensors(**state, **config)
    runClient(**state, **config)
    runServer(**state, **config)

    return state

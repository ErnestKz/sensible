# Author: Ernest and Wanying

import os
import time
import threading
from pprint import pprint
from sensible.database import selectDataAll, selectOtherDataAll, selectDataSummary, selectOtherDataSummary

def runBaseInterface(virtualDevices):
    devicesString = "Virtual devices running on ports: " + str(list(virtualDevices.keys()))
    print(devicesString)
    while True:
        i = input(f"(BASE) >> ")
        if i == "clear":
            os.system('clear')
        if "device " in i:
            port = int(i[len("device "):])
            if port in virtualDevices.keys():
                device = virtualDevices[port]
                config, state = device["config"], device["state"]
                print("Entering shell of virtual device of port: ", port)
                getInterface(**config, **state)()
            else:
                print("Virtual device does not exist on port: ", port)
        if "devices" == i:
            print(devicesString)

def getInterface(lock, data, otherData, clientLog, serverLog, port, deviceAddress, **kwargs):
    def runInterface():
        while True:
            databaseData = selectDataAll(deviceAddress)
            databaseOtherData = selectOtherDataAll(deviceAddress)
            i = input(f"(DEVICE:{port}) >> ")
            if i == "clear":
                os.system('clear')
            if i == "all":
                # displayStats(data, otherData, clientLog, serverLog)
                displayStats(databaseData, databaseOtherData, clientLog, serverLog)
            if i == "received_data":
                # pprint(otherData)
                pprint(databaseOtherData)
            if i == "received_summary":
                # createSummaryReceivedData(otherData)
                receivedDataSummary = selectOtherDataSummary(deviceAddress)
                pprint(receivedDataSummary)
            if i == "sensed_data":
                # pprint(data)
                pprint(databaseData)
            if i == "sensed_summary":
                # createSummarySensedData(data)
                sensedDataSummary = selectDataSummary(deviceAddress)
                pprint(sensedDataSummary)

            if i == "exit":
                break
    return runInterface

def createSummaryReceivedData(otherData):
    for peer, sensor_data in otherData.items(): 
        print(peer)
        for sensor_name, sensed_data in sensor_data.items(): 
            print("\t", sensor_name, ":", len(sensed_data))
            
def createSummarySensedData(data):
    for sensor_name, sensed_data in data.items(): 
            print(sensor_name, ":", len(sensed_data))

def displayStats(data, otherData, clientLog, serverLog):
    print("data:", data)
    print("====================================================================================")
    print("otherData:", otherData)
    print("====================================================================================")
    print("clientLog:", clientLog)
    print("====================================================================================")
    print("serverLog", serverLog)

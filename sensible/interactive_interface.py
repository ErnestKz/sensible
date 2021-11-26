import os
import time
import threading

def runBaseInterface(piShells):
    devicesString = "Virtual devices running on ports: " + str(list(piShells.keys()))
    print(devicesString)
    while True:
        i = input(f"(BASE) >> ")
        if i == "clear":
            os.system('clear')
        if "device " in i:
            port = int(i[len("device "):])
            if port in piShells.keys():
                print("Entering shell of virtual device of port: ", port)
                piShells[port]()
            else:
                print("Virtual device does not exist on port: ", port)
        if "devices" == i:
            print(devicesString)

def getInterface(lock, data, otherData, clientLog, serverLog, port):
    def runInterface():
        # threading.Thread(target=runStats, args=(data, otherData, clientLog, serverLog)).start()
        while True:
            i = input(f"(DEVICE:{port}) >> ")
            if i == "clear":
                os.system('clear')
            if i == "all":
                displayStats(data, otherData, clientLog, serverLog)
            if i == "exit":
                break
    return runInterface

def displayStats(data, otherData, clientLog, serverLog):
    print("data:", data)
    print("====================================================================================")
    print("otherData:", otherData)
    print("====================================================================================")
    print("clientLog:", clientLog)
    print("====================================================================================")
    print("serverLog", serverLog)

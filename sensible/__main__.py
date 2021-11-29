import argparse
import time

from . import runNode
from sensible.interactive_interface import runBaseInterface
from sensible.node import createConfig
from sensible.sensors import virtual_sensors

def main() -> None: 
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", type=str)
    args = parser.parse_args()
    print(args.mode)
    # modes are: pi25, pi26, and virtual
    
    virtualDevices = {}
    if (args.mode == "virtual"):
        basePort = 8000
        numNodes = 3
        # peers = [("localhost", 8000), ("localhost", 8001), ("timeout.org", 8001)]
        peers1 = [("localhost", 8001), ("localhost", 8002)]
        peers2 = [("localhost", 8000), ("localhost", 8002)]
        peers3 = [("localhost", 8000), ("localhost", 8001)]
        peers = [peers1, peers2, peers3]
        toAddress = lambda l : list(map(lambda p: f'http://{p[0]}:{p[1]}', l))
        addresses = list(map(toAddress, peers))
        
        for n in range(numNodes):
            devicePort = basePort + n
            i = (n*3)
            deviceConfig = createConfig(devicePort,
                                        addresses[n],
                                        [virtual_sensors[i], virtual_sensors[i+1], virtual_sensors[i+2]])
            deviceState = runNode(deviceConfig)
            virtualDevices[devicePort] = { "config": deviceConfig,
                                           "state": deviceState }
        runBaseInterface(virtualDevices)
    else:
        toAddress = lambda p: f'http://{p[0]}:{p[1]}'
        port = 8009
        pi25 = toAddress(("rasp-025.berry.scss.tcd.ie ", port))
        pi26 = toAddress(("rasp-026.berry.scss.tcd.ie ", port))
        
        if (args.mode == "pi25"):
            peers = [pi26]
            sensors = [virtual_sensors[0], virtual_sensors[1], virtual_sensors[2]]
        elif (args.mode == "pi26"):
            peers = [pi25]
            sensors = [virtual_sensors[3], virtual_sensors[4], virtual_sensors[5]]
            
        deviceConfig = createConfig(port, peers, sensors)
        deviceState = runNode(deviceConfig)
        virtualDevices[devicePort] = { "config": deviceConfig,
                                       "state": deviceState }
        runBaseInterface(virtualDevices)
            
        
if __name__ == "__main__":
    main()
    
# Running this on a Pi:
# As a single node:
#  Runs:
#   - Sensors
#   - Client
#   - Server
#   - Runs Shell to Evaluate Python code
#     - 'data' will a variable to query.

# As n nodes
# Same as above but for n nodes
#   - But now the shell allows to pick which pi to log into.
#   - When in the shell can exit it with predefined function.


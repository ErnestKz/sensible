import argparse
import time

from . import runNode
from sensible.interactive_interface import runBaseInterface
from sensible.node import createConfig
from sensible.sensors import virtual_sensors

# read in arguments with argParss


pi25 = ("rasp-025.berry.scss.tcd.ie ", 8006)
pi25 = ("rasp-026.berry.scss.tcd.ie ", 8006)

def main() -> None: 
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", type=str)
    args = parser.parse_args()
    print(args.mode)
    # modes are: pi25, pi26, and virtual

    basePort = 8000
    numNodes = 3
    # peers = [("localhost", 8000), ("localhost", 8001), ("timeout.org", 8001)]
    peers1 = [("localhost", 8001), ("localhost", 8002)]
    peers2 = [("localhost", 8000), ("localhost", 8002)]
    peers3 = [("localhost", 8000), ("localhost", 8001)]
    peers = [peers1, peers2, peers3]

    toAddress = lambda l : list(map(lambda p: f'http://{p[0]}:{p[1]}', l))
    addresses = list(map(toAddress, peers))

    print(addresses)
    
    virtualDevices = {}
    for n in range(numNodes):
        devicePort = basePort + n

        i = (n*3)
        deviceConfig = createConfig(devicePort,
                                    addresses[n],
                                    [virtual_sensors[i], virtual_sensors[i+1], virtual_sensors[i+2]])
                                    
        deviceState = runNode(deviceConfig)
        
        virtualDevices[devicePort] = { "config": deviceConfig,
                                       "state": deviceState
                                      }
        
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


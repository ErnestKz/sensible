import argparse
import time

from . import runNode
from sensible.interactive_interface import runBaseInterface
from sensible.node import createConfig
from sensible.sensors import virtual_sensors

# read in arguments with argParss

def main() -> None: 
    parser = argparse.ArgumentParser(description="sensible.", epilog="Enjoy the sensible functionality!")
    args = parser.parse_args()
    
    basePort = 8000
    numNodes = 3
    peers = [("localhost", 8000), ("localhost", 8001), ("timeout.org", 8001)]
    
    addresses = list(map(lambda p: f'http://{p[0]}:{p[1]}', peers))
    
    virtualDevices = {}
    for n in range(numNodes):
        devicePort = basePort + n

        deviceConfig = createConfig(devicePort, addresses, [virtual_sensors[n],
                                                            virtual_sensors[n+1],
                                                            virtual_sensors[n+2]])
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


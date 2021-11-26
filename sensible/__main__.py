import argparse
import time

from . import runNode
from sensible.interactive_interface import runBaseInterface

def main() -> None: 
    parser = argparse.ArgumentParser(description="sensible.", epilog="Enjoy the sensible functionality!")
    args = parser.parse_args()

    basePort = 8000
    numNodes = 3
    piShells = {}
    
    for n in range(numNodes):
        piPort = basePort + n
        piShell = runNode(piPort)
        piShells[piPort] = piShell
        
    runBaseInterface(piShells)
        
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


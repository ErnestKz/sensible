# sensible
[Project Report](./Report.pdf)

## Install

## Instructions
The main configurations available for demo are:
- To run this program as multiple nodes on the same machine. This config aims to demonstrate interactive shell and the ability to inspect and operate on the data that a node has received from other nodes.
- To run the program as a single node intended to communicate across the network. This config demonstrates the ability for nodes (in this case Raspberry Pis) to communicate across a network.

### Multiple Nodes on Single Machine: The Interactive Shell
The command:  
```python -m sensible virtual```

### Single Node: Communication Across Network
For the demo, communication across 2 pis is configured.
Once the code is installed on both of the pis.
On one pi, 
```python -m sensible pi25```
is run, and on the other,
```python -m sensible pi26```
Communication can be observed across the network between the pis by using the shell.
## Interactive Shell Commands
### Top-Level Shell
When you first enter the shell, the shell prompt will look
something like:
```(BASE) >> ```  
This indicates that you are at the "Top-Level" of the shell.  
The commands available in this shell are:
- `device <number>` Where `<number>` is the port of the device you want to attatch to.
- `devices` This will list all the device port numbers available to attatch to.

### Device-Level Shell
When the shell is attatched to a device, the shell prompt will look
something like:
```(DEVICE:8000) >> ```
In this case, the shell is attatched to the device listening on port 8000.  
The commands available in this shell are:
- `clear` To clear the terminal.
- `all` To show all of the data in the database.
- `received_data` To show all of that data that has been received from other devices.
- `sensed_data` To show all of the data that the current device has sensed.
- `received_summary` To show a summary of received data, i.e how many data points sensed per sensor of devices.
- `sensed_summary` To show a summary of sensed data, i.e how many data points sensed per sensor of the current device.
- `exit` To detach from the current device and enter the Top-Level shell.


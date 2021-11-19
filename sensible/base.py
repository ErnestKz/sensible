"""
sensible base module.

This is the principal module of the sensible project.
here you put your main classes and objects.
"""


# Device:
# - One flexible core protocol.
#   - Can extablish details about communication to other devices.

# - The device simply accumulates information of the world by collecting  sensor data from other devices.
# - Other devices can share the sensor data that they have collected from other devices aswell.

# Core functionality:
# - Discover other devices.
# - Establish communication protocol with them.
#   - The resulting communication protocol is set by the user depending on requirements.
#   - The resulting communciation protocol is also dependent on the other device.
# - Recieve, send, and store sensor data.
# - The stored sensor data can be queried and inspected.


# Communication Channels and Device Discovery:
# - Will need to support communicating across the network to devices.
# - Will need to support broadcasting existence/ scanning for devices.

# - Will need to support simulating devices.
#   - Can do so just by using the same device on a different port.

# - Perhaps can specify where to scan.
#   - Can give a list of IP's and ports to scan over.
# - Communicate over ports.
#   - Using the flexible core protocol.

# Protocol:


# Storage:

import socket
import selectors


class BaseClass:
    def base_method(self) -> str:
        """
        Base method.
        """
        return "hello from BaseClass"

    def __call__(self) -> str:
        return self.base_method()

# The command:
# netstat -an
# will show you state of the sockets on the device.
# another way is
# lsof -i -n
def base_echo_server() -> None:
    """
    base_echo_server :: IO ()
    """
    HOST = '127.0.0.1'  
    PORT = 65432
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # SOCK_STREAM means TCP
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept() # conn is now a socket that is distinct from the socket listening to accept new connections.
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024) # maximum amount of data to be received at once.
                if not data:
                    break
                conn.sendall(data)
                # send returns number of bytes sent, you are responsiblefor calling send() as many times as needed to send all of the data.
                # soe we use sendall to avoid this
    return None

def base_echo_client() -> None:
    """
    base_echo_client :: IO ()
    """
    HOST = '127.0.0.1'  
    PORT = 65432
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        msg = b'Hello, world!'
        # print(len(msg))
        s.sendall(msg)
        data = s.recv(1024)

    print("Received", repr(data))
    return None

# Multi-Connection Server:
def base_echo_server_multi() -> None:
    """
    base_echo_server_multi :: IO ()
    """
    HOST = '127.0.0.1'  
    PORT = 65432

    sel = selectors.DefaultSelector()
    # ....
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind((HOST, PORT))
    lsock.listen()
    print("Listening on", (HOST, PORT))
    lsock.setblocking(False)
    # socket is in non-blocking mode, no longer blocks
    
    sel.register(lsock, selectors.EVENT_READ, data=None)
    # registers the socket to be monitored with sel.select() for events we're interested in
    # for the listening socket, we want read events selectors.EVENT_READ
    # data is used to store arbitrary data along with the socket
    
    return None
    
def base_event_loop() -> None:
    sel = selectors.DefaultSelector()
    # ...
    while True:
        events = sel.select(timeout=None) # Blocks until there are sockets ready for IO
        for key, mask in events:           
            if key.data is None:            # data is the data that what we attatched to the event
                accept_wrapper(key.fileobj) # fileobj is the socket object
                # call our accept(), to get new socket object and register with the selector
            else:
                service_connection(key, mask) # This services the accepted connection
    
def accept_wrapper(sock) -> None:
    conn, addr = sock.accept()  # should be ready to read
    print("Accepted connection from", addr)
    conn.setblocking(False)

    # we create an object to hold data we want included along with the socket
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask) -> None:
    sock = key.fileobj
    data = key.data
    # looks like the mask that we pass will always read and then write
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024) # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            print("Closing connection to", data_addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print("Echoing", repr(data.outb), 'to', data.addr)
            sent = sock.send(data.outb) # Should be ready to write
            data.outb = data.outb[sent:]
    
# MultiConnection Client:
messages = [b'Message 1 from client.', b'Message 2 from client.']

def client_start_connections(host, port, num_conns):
    server_addr = (host, port)
    for i in range(0, num_conns):
        connid = i + 1
        print("Starting connection", connid, "to", server_addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(connid=connid,
                                     msg_total=sum(len(m) for m in messages),
                                     recv_total=0,
                                     messages=list(messages),
                                     outb=b'')
        sel.register(sock, events, data=data)
        
            
def client_service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024) # should be ready to read
        if recv_data:
            print('received', repr(recv_data), 'from connection', data.connid)
            data.recv_total += len(recv_data)
        if not recv_data or data.recv_total == data.msg_total:
            print('closing connection', data.connid)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
        if data.outb:
            print('sending', repr(data.outb), 'to connection', data.connid)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]
    
# Client keeps track the number of bytes it's received from the server so it
# can close its side of the connection.
# When the server detects this, it closes its side of the connection too.
# This depends on the client being well behaved

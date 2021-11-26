import requests
import time
import json
import threading

def runClient(lock, otherData, clientLog):
    threading.Thread(target=clientLoop, args=(lock, otherData, clientLog)).start()

def clientLoop(lock, otherData, clientLog):
    peers = [("localhost", 8000), ("localhost", 8001), ("timeout.org", 8001)]
    peerAddresses = list(map(createUrl, peers))
    peersLastRequested = {}
    
    while True:
        # Can try put each of these requests in a separate thread.
        for peer in peerAddresses:
            try:
                timePreviousRequest = peersLastRequested[peer] if peer in peersLastRequested.keys() else 0
                msg = { "lastRequest": timePreviousRequest }
                msg = json.dumps(msg)
                
                # perhaps a lock here
                timeCurrentRequest = time.time()
                r = requests.post(peer, data=msg, timeout=2)
                
                clientLog.append(f'Sent to: {peer}, code {r.status_code}')
                
                otherData = storeData(otherData, r.json())
                peersLastRequested[peer] = timeCurrentRequest
            except requests.exceptions.RequestException as e:
                clientLog.append(f'Connection failed to: {peer}')
        time.sleep(2)

def storeData(collected, new):
    for i in new:
        if i in collected:
            collected[i].extend(new[i])
        else:
            collected[i] = new[i]
    return collected        
        
def createUrl(dst):
    (addr, port) = dst
    return f'http://{addr}:{port}'

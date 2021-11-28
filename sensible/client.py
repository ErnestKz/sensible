import requests
import time
import json
import threading

def runClient(lock, otherData, clientLog, addresses, **kwargs):
    threading.Thread(target=clientLoop, args=(lock, otherData, clientLog, addresses)).start()

def clientLoop(lock, otherData, clientLog, addresses):
    
    peersLastRequested = {}
    while True:
        # Can try put each of these requests in a separate thread.
        for peer in addresses:
            try:
                timePreviousRequest = peersLastRequested[peer] if peer in peersLastRequested.keys() else 0
                msg = { "lastRequest": timePreviousRequest }
                msg = json.dumps(msg)
                
                # perhaps a lock here
                timeCurrentRequest = time.time()
                r = requests.post(peer, data=msg, timeout=2)
                
                clientLog.append(f'Sent to: {peer}, code {r.status_code}')
                
                otherData = storeData(peer, otherData, r.json())
                peersLastRequested[peer] = timeCurrentRequest
            except requests.exceptions.RequestException as e:
                clientLog.append(f'Connection failed to: {peer}')
        time.sleep(2)

def storeData(peer, collected, new):
    if peer not in collected:
        collected[peer] = {}

    for i in new:
        if i in collected[peer]:
            collected[peer][i].extend(new[i])
        else:
            collected[peer][i] = new[i]
    return collected        
        


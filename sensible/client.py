import requests
import time
import json
import threading
from sensible.database import insertOtherData

def runClient(lock, otherData, clientLog, deviceAddress, addresses, **kwargs):
    threading.Thread(target=clientLoop, args=(lock, otherData, clientLog, deviceAddress, addresses)).start()

def clientLoop(lock, otherData, clientLog, deviceAddress, addresses):
    peersLastRequested = {}
    
    session = requests.Session()
    session.trust_env = False
    while True:
        # Can try put each of these requests in a separate thread.
        for peer in addresses:
            try:
                timePreviousRequest = peersLastRequested[peer] if peer in peersLastRequested.keys() else 0
                msg = { "lastRequest": timePreviousRequest }
                msg = json.dumps(msg)
                
                # perhaps a lock here

                
        
                timeCurrentRequest = time.time()
                
                # r = session.prepare_request(requests.Request('POST', peer, data=msg, timeout=2))
                r = session.post(peer, data=msg, timeout=2)
                
                clientLog.append(f'Sent to: {peer}, code {r.status_code}')
                
                otherData = storeData(deviceAddress, peer, otherData, r.json())
                peersLastRequested[peer] = timeCurrentRequest
            except requests.exceptions.RequestException as e:
                clientLog.append(f'Connection failed to: {peer}')
        time.sleep(2)

def storeData(deviceAddress, peer, collected, new):
    if peer not in collected:
        collected[peer] = {}

    for i in new:
        if i in collected[peer]:
            collected[peer][i].extend(new[i])
        else:
            collected[peer][i] = new[i]
        for data in new[i]:
            insertOtherData(deviceAddress, peer, i, data['data'], data['timestamp'])
    return collected        
        


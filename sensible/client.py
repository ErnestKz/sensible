import requests
import time
import json

peers = [("localhost", 8000), ("localhost", 8001), ("timeout.org", 8001)]

sample_msg = {
    "id": "superid",
    "data": {
        "fruit": "apple",
        "veg": "carrot"
    }
}

def httpClient():
    msg = json.dumps(sample_dataset)
    r = requests.post('http://localhost:8000', data = msg)
    print(r.status_code)
    print(r.json())
    
def clientLoop():
    while True:
        # Can try put each of these requests in a separate thread.
        for peer in peers:
            url = createUrl(peer)
            try:
                msg = json.dumps(sample_msg)
                r = requests.post(url, data=msg, timeout=2)
                print("Sent to", peer, "status code", r.status_code)
                print(r.json())
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                print("Connection failed to:", url)
                
        time.sleep(2)
        
def createUrl(dst):
    (addr, port) = dst
    return f'http://{addr}:{port}'

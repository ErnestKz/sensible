import random

import requests
import http.server as http
import json
import threading
import time

def httpClient(sensor):
    msg = json.dumps({'sensor':sensor})
    r = requests.post('http://localhost:8000', data = msg)
    print(r.status_code)
    print(r.json())


class Handler(http.BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
    def do_HEAD(self):
        self._set_headers()
        
    def do_GET(self):
        self._set_headers()
        global data
        temp = data['temperature']
        msg = json.dumps(temp)
        msg = bytes(msg, 'utf-8')
        self.wfile.write(msg)
        
    def do_POST(self):
        self._set_headers()
        length = int(self.headers.get('Content-Length'))
        msg = self.rfile.read(length)
        print(msg)
        msg = json.loads(msg)
        requestSensor = msg['sensor']
        global data
        msg = data[requestSensor]
        # process message ...
        msg = json.dumps(msg)
        msg = bytes(msg, 'utf-8')
        self.wfile.write(msg)

def httpServer(server_class=http.HTTPServer, handler_class=Handler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

data = {}
lock = threading.Lock()
def sensor_temp(sleep):
    while True:
        lock.acquire()
        global data
        temp_dic = {}
        temp = random.randint(7,23)
        temp_dic['data'] = temp
        temp_dic['timestamp'] = time.time()
        if 'temperature' in data.keys():
            data['temperature'].append(temp_dic)
        else:
            data['temperature'] = [temp_dic]
        print(data)
        lock.release()
        time.sleep(sleep)

def sensor_motion(sleep):
    while True:
        lock.acquire()
        global data
        temp_dic = {}
        motion = random.getrandbits(1)
        temp_dic['data'] = motion
        temp_dic['timestamp'] = time.time()
        if 'motion' in data.keys():
            data['motion'].append(temp_dic)
        else:
            data['motion'] = [temp_dic]
        lock.release()
        time.sleep(sleep)

possible_humans = ["John", "Alex", "Mary", "Vasya", "Unknwon"]
def sensor_human(sleep):
    while True:
        lock.acquire()
        global data
        temp_dic = {}
        num_humans = random.randint(0, 2)
        humans = random.sample(possible_humans, num_humans)
        temp_dic['data'] = humans
        temp_dic['timestamp'] = time.time()
        if 'human' in data.keys():
            data['human'].append(temp_dic)
        else:
            data['human'] = [temp_dic]
        lock.release()
        time.sleep(sleep)

def sensor_light(sleep):
    while True:
        lock.acquire()
        global data
        temp_dic = {}
        light = random.uniform(0.00001,100000)
        temp_dic['data'] = light
        temp_dic['timestamp'] = time.time()
        if 'lightLevel' in data.keys():
            data['lightLevel'].append(temp_dic)
        else:
            data['lightLevel'] = [temp_dic]
        lock.release()
        time.sleep(sleep)


if __name__=='__main__':
    t1 = threading.Thread(target=sensor_temp,args=(1,))
    t2 = threading.Thread(target=sensor_motion,args=(2,))
    t3 = threading.Thread(target=sensor_human,args=(1.5,))
    t4 = threading.Thread(target=sensor_light, args=(2,))
    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t5 = threading.Thread(target=httpServer)
    t5.start()
    while True:
        print(data)
        time.sleep(1)
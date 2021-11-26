import random
import http.server as http
import json
import threading
import time

def runServer(lock, data, serverLog, port):
    threading.Thread(target=httpServer, args = (lock, data, serverLog, port)).start()

def httpServer(lock, data, serverLog, port):
    server_address = ('', port)
    server_class=http.HTTPServer
    httpd = server_class(server_address, createHandler(lock, data, serverLog))
    httpd.serve_forever()
    
def createHandler(lock, data, serverLog):
    class Handler(http.BaseHTTPRequestHandler):
        def _set_headers(self):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

        def log_message(self, format, *args):
            return
        
        def do_POST(self):
            self._set_headers()
            serverLog.append("Processing")
            
            length = int(self.headers.get('Content-Length'))
            msg = self.rfile.read(length)
            msg = json.loads(msg)
            serverLog.append(msg)
            requestLast = msg['lastRequest']

            # might need to add a lock here
            msg = {}
            for i in data:
                temp_list = []
                for j in data[i]:
                    if j['timestamp'] > requestLast:
                        temp_list.append(j)
                msg[i] = temp_list

            msg = json.dumps(msg)
            msg = bytes(msg, 'utf-8')
            self.wfile.write(msg)
    return Handler

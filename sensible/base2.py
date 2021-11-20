import requests
import http.server as http
import json

sample_dataset = {
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


class Handler(http.BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
    def do_HEAD(self):
        self._set_headers()
        
    def do_GET(self):
        self._set_headers()
        msg = json.dumps({'hello': 'world', 'received': 'ok'})
        msg = bytes(msg, 'utf-8')
        self.wfile.write(msg)
        
    def do_POST(self):
        self._set_headers()
        length = int(self.headers.get('Content-Length'))
        msg = self.rfile.read(length)
        print(msg)
        msg = json.loads(msg)
        # process message ...
        msg = json.dumps(msg)
        msg = bytes(msg, 'utf-8')
        self.wfile.write(msg)

def httpServer(server_class=http.HTTPServer, handler_class=Handler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


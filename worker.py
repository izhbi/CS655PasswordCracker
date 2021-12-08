from itertools import product
from string import ascii_lowercase
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import threading
import hashlib
import socket

class WorkerServer(BaseHTTPRequestHandler):
    def crack_password(self, hash, startChar, endChar):
        for c in range(ord(startChar), ord(endChar) + 1):
            for e in product(ascii_lowercase,repeat=4):
                candidate = chr(c) + ''.join(e)
                if (hashlib.md5(candidate.encode()).hexdigest() == hash.lower()):
                    return candidate
        
        return None
    
    def do_GET(self):
        inputs = self.path.split('/')
        response = "Invalid input"
        if (len(inputs) == 3 and len(inputs[1]) == 32 and len(inputs[2]) == 2):
            result = self.crack_password(inputs[1], inputs[2][0], inputs[2][1])
            response = result if result is not None else "Not found"
        
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(response, "utf-8"))

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass

HOST = "0.0.0.0" #socket.gethostname()
PORT = 9007

def run():
    webServer = ThreadingSimpleServer((HOST, PORT), WorkerServer)
    print("Worker server started %s:%s" % (HOST, PORT))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Stopping worker server")

if __name__ == "__main__":
    run()
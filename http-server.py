import socket
import subprocess
from http.server import BaseHTTPRequestHandler,HTTPServer

hostName = socket.gethostname()
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.strip("/").split("/")
        if path[0] == "":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            with open("index.html", "r") as f:
                self.wfile.write(bytes(f.read(), "utf-8"))
        elif path[0] == "break":
            md5hash = path[1]
            num_workers = int(path[2])
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            
            result = subprocess.run(['python', 'manager.py', md5hash, str(num_workers)], stdout=subprocess.PIPE).stdout.decode('ASCII')
            self.wfile.write(bytes(result, "utf-8"))

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
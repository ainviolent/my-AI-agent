from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            status = 200
            body = "Hello from Ubuntu Server"
        elif self.path == "/health":
            status = 200
            body = "OK"
        elif self.path == "/time":
            status = 200
            body = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elif self.path == "/about":
            status = 200
            body = "Practice service"
        else:
            status = 404
            body = "Not found"

        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

HTTPServer(("127.0.0.1", 8765), Handler).serve_forever()


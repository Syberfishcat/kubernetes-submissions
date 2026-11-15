import os
from http.server import HTTPServer, BaseHTTPRequestHandler

counter = 0


class PingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global counter
        if self.path != "/pingpong":
            self.send_error(404, "Not Found")
            return
        body = f"pong {counter}".encode()
        counter += 1
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


port = int(os.environ.get("PORT", "3000"))
print(f"Server started in port {port}", flush=True)
HTTPServer(("0.0.0.0", port), PingHandler).serve_forever()

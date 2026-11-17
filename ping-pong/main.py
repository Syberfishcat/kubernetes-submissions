import os
from http.server import HTTPServer, BaseHTTPRequestHandler

counter = 0


class PingHandler(BaseHTTPRequestHandler):
    def respond(self, body):
        body = body.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        global counter
        if self.path == "/pingpong":
            body = f"pong {counter}"
            counter += 1
            self.respond(body)
        elif self.path == "/pings":
            self.respond(str(counter))
        else:
            self.send_error(404, "Not Found")


port = int(os.environ.get("PORT", "3000"))
print(f"Server started in port {port}", flush=True)
HTTPServer(("0.0.0.0", port), PingHandler).serve_forever()

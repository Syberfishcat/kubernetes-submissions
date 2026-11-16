import os
from http.server import HTTPServer, BaseHTTPRequestHandler

LOG_DIR = os.environ.get("LOG_DIR", "/app/logs")
COUNT_FILE = os.path.join(LOG_DIR, "pingpong.txt")


def load_counter():
    try:
        with open(COUNT_FILE) as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0


def save_counter(value):
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(COUNT_FILE, "w") as f:
        f.write(str(value))


counter = load_counter()


class PingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global counter
        if self.path != "/pingpong":
            self.send_error(404, "Not Found")
            return
        body = f"pong {counter}".encode()
        counter += 1
        save_counter(counter)
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


port = int(os.environ.get("PORT", "3000"))
print(f"Server started in port {port}", flush=True)
HTTPServer(("0.0.0.0", port), PingHandler).serve_forever()

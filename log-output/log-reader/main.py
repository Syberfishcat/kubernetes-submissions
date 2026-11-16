import os
from http.server import HTTPServer, BaseHTTPRequestHandler

LOG_DIR = os.environ.get("LOG_DIR", "/app/logs")
LOG_FILE = os.path.join(LOG_DIR, "log.txt")
COUNT_FILE = os.path.join(LOG_DIR, "pingpong.txt")


def read_last_line(path):
    try:
        with open(path) as f:
            lines = f.read().splitlines()
        return lines[-1] if lines else ""
    except FileNotFoundError:
        return ""


def read_count(path):
    try:
        with open(path) as f:
            return f.read().strip() or "0"
    except FileNotFoundError:
        return "0"


class LogHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            self.send_error(404, "Not Found")
            return
        body = f"{read_last_line(LOG_FILE)}\nPing / Pongs: {read_count(COUNT_FILE)}\n".encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


HTTPServer(("0.0.0.0", int(os.environ.get("PORT", "8080"))), LogHandler).serve_forever()

import os
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

LOG_DIR = os.environ.get("LOG_DIR", "/app/logs")
LOG_FILE = os.path.join(LOG_DIR, "log.txt")
PINGS_URL = os.environ.get("PINGS_URL", "http://ping-pong-svc:2345/pings")
CONFIG_FILE = os.environ.get("CONFIG_FILE", "/config/information.txt")


def read_file(path):
    try:
        with open(path) as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""


def read_last_line(path):
    try:
        with open(path) as f:
            lines = f.read().splitlines()
        return lines[-1] if lines else ""
    except FileNotFoundError:
        return ""


def read_count():
    try:
        with urllib.request.urlopen(PINGS_URL, timeout=3) as r:
            return r.read().decode().strip()
    except Exception:
        return "0"


class LogHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            self.send_error(404, "Not Found")
            return
        
        body = (
            f"file content: {read_file(CONFIG_FILE)}\n"
            f"env variable: MESSAGE={os.environ.get('MESSAGE', '')}\n"
            f"{read_last_line(LOG_FILE)}\n"
            f"Ping / Pongs: {read_count()}\n"
        ).encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


HTTPServer(("0.0.0.0", int(os.environ.get("PORT", "8080"))), LogHandler).serve_forever()

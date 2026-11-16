import os
from http.server import HTTPServer, BaseHTTPRequestHandler

LOG_FILE = os.path.join(os.environ.get("LOG_DIR", "/app/logs"), "log.txt")


class LogHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            self.send_error(404, "Not Found")
            return
        try:
            with open(LOG_FILE, "rb") as f:
                body = f.read()
        except FileNotFoundError:
            body = b""
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


HTTPServer(("0.0.0.0", int(os.environ.get("PORT", "8080"))), LogHandler).serve_forever()

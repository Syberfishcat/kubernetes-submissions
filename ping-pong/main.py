import os
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

import psycopg

DATABASE_URL = os.environ["DATABASE_URL"]


def db():
    return psycopg.connect(DATABASE_URL, autocommit=True)


# Wait until the database accepts connections
while True:
    try:
        with db() as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS counter (value INT NOT NULL)")
            if conn.execute("SELECT COUNT(*) FROM counter").fetchone()[0] == 0:
                conn.execute("INSERT INTO counter VALUES (0)")
        break
    except psycopg.OperationalError:
        print("Database not ready, retrying...", flush=True)
        time.sleep(2)


class PingHandler(BaseHTTPRequestHandler):
    def respond(self, body):
        body = body.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/pingpong":
            with db() as conn:
                count = conn.execute("SELECT value FROM counter").fetchone()[0]
                conn.execute("UPDATE counter SET value = value + 1")
            self.respond(f"pong {count}")
        elif self.path == "/pings":
            with db() as conn:
                count = conn.execute("SELECT value FROM counter").fetchone()[0]
            self.respond(str(count))
        else:
            self.send_error(404, "Not Found")


port = int(os.environ.get("PORT", "3000"))
print(f"Server started in port {port}", flush=True)
HTTPServer(("0.0.0.0", port), PingHandler).serve_forever()
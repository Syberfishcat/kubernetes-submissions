import json
import os
import time
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

import psycopg

MAX_LEN = int(os.environ["TODO_MAX_LENGTH"])
DATABASE_URL = os.environ["DATABASE_URL"]
INITIAL_TODOS = ["Learn Kubernetes basics", "Deploy application to cluster", "Configure persistent volumes"]


def db():
    return psycopg.connect(DATABASE_URL, autocommit=True)


# Wait until the database accepts connections, then create the table
while True:
    try:
        with db() as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS todos (id SERIAL PRIMARY KEY, text TEXT NOT NULL)")
            if conn.execute("SELECT COUNT(*) FROM todos").fetchone()[0] == 0:
                for todo in INITIAL_TODOS:
                    conn.execute("INSERT INTO todos (text) VALUES (%s)", (todo,))
        break
    except psycopg.OperationalError:
        print("Database not ready, retrying...", flush=True)
        time.sleep(2)


class TodoHandler(BaseHTTPRequestHandler):
    def respond(self, code, payload):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path != "/todos":
            self.send_error(404, "Not Found")
            return
        with db() as conn:
            rows = conn.execute("SELECT text FROM todos ORDER BY id").fetchall()
        self.respond(200, [row[0] for row in rows])

    def do_POST(self):
        if self.path != "/todos":
            self.send_error(404, "Not Found")
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            data = json.loads(self.rfile.read(length) or b"{}")
            text = str(data["todo"]).strip()
        except (ValueError, KeyError, TypeError):
            print(f"Rejected todo: invalid body", flush=True)
            self.respond(400, {"error": "Body must be JSON like {\"todo\": \"...\"}"})
            return
        if not text or len(text) > MAX_LEN:
            print(f"Rejected todo: ({len(text)} chars): {text}", flush=True)
            self.respond(400, {"error": f"Todo must be 1-{MAX_LEN} characters"})
            return
        with db() as conn:
            conn.execute("INSERT INTO todos (text) VALUES (%s)", (text,))
            print(f"Created todo: {text}", flush=True)
        self.respond(201, {"todo": text})


port = int(os.environ["PORT"])
print(f"Server started in port {port}", flush=True)
ThreadingHTTPServer(("0.0.0.0", port), TodoHandler).serve_forever()

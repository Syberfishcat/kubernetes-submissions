import json
import os
import threading
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

MAX_LEN = int(os.environ["TODO_MAX_LENGTH"])
todos = ["Learn Kubernetes basics", "Deploy application to cluster", "Configure persistent volumes"]
lock = threading.Lock()


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
        with lock:
            self.respond(200, todos)

    def do_POST(self):
        if self.path != "/todos":
            self.send_error(404, "Not Found")
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            data = json.loads(self.rfile.read(length) or b"{}")
            text = str(data["todo"]).strip()
        except (ValueError, KeyError, TypeError):
            self.respond(400, {"error": "Body must be JSON like {\"todo\": \"...\"}"})
            return
        if not text or len(text) > MAX_LEN:
            self.respond(400, {"error": f"Todo must be 1-{MAX_LEN} characters"})
            return
        with lock:
            todos.append(text)
        self.respond(201, {"todo": text})


port = int(os.environ["PORT"])
print(f"Server started in port {port}", flush=True)
ThreadingHTTPServer(("0.0.0.0", port), TodoHandler).serve_forever()

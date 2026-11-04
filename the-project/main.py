import os
from http.server import HTTPServer, BaseHTTPRequestHandler


class TodoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            self.send_error(404, "Not Found")
            return

        body = b"<h1>Todo app</h1><p>Hello from Kubernetes!</p>"
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


port = int(os.environ.get("PORT", "8080"))
server = HTTPServer(("0.0.0.0", port), TodoHandler)
print(f"Server started in port {port}", flush=True)
server.serve_forever()
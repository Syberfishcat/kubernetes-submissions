import os
from http.server import HTTPServer, BaseHTTPRequestHandler

port = int(os.environ.get("PORT", "8080"))

server = HTTPServer(("0.0.0.0", port), BaseHTTPRequestHandler)

print(f"Server started in prot {port}", flush=True)

server.serve_forever()
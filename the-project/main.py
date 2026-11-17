import os
import threading
import time
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

IMAGE_DIR = os.environ.get("IMAGE_DIR", "/app/images")
IMAGE_PATH = os.path.join(IMAGE_DIR, "image.jpg")
IMAGE_URL = "https://picsum.photos/1200"
MAX_AGE = 10 * 60  # seconds

lock = threading.Lock()


def fetch_image():
    os.makedirs(IMAGE_DIR, exist_ok=True)
    req = urllib.request.Request(IMAGE_URL, headers={"User-Agent": "todo-app"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = resp.read()
    tmp = IMAGE_PATH + ".tmp"
    with open(tmp, "wb") as f:
        f.write(data)
    os.replace(tmp, IMAGE_PATH)  # atomic, so readers never see a half-written file
    print("Fetched new image", flush=True)


def get_image():
    """Return cached image bytes. If the cache is older than MAX_AGE, serve the
    old one one last time and fetch a new one for the next request."""
    with lock:
        if not os.path.exists(IMAGE_PATH):
            fetch_image()
        with open(IMAGE_PATH, "rb") as f:
            data = f.read()
        if time.time() - os.path.getmtime(IMAGE_PATH) > MAX_AGE:
            try:
                fetch_image()
            except Exception as e:
                print(f"Image refresh failed: {e}", flush=True)
        return data


class TodoHandler(BaseHTTPRequestHandler):
    def respond(self, code, ctype, body):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            html = (
                "<!DOCTYPE html><html><head><meta charset='utf-8'>"
                "<title>Todo App</title>"
                "<style>"
                "body{font-family:Helvetica,Arial,sans-serif;text-align:center;margin:40px;}"
                "h1{color:#333;}"
                "img{width:460px;max-width:100%;border-radius:8px;"
                "box-shadow:0 2px 8px rgba(0,0,0,.3);}"
                "p{color:#777;}"
                "</style></head><body>"
                "<h1>Todo App</h1>"
                '<img src="/image">'
                "<p>DevOps with Kubernetes 2026</p>"
                "</body></html>"
            )
            self.respond(200, "text/html; charset=utf-8", html.encode())
        elif self.path == "/image":
            try:
                self.respond(200, "image/jpeg", get_image())
            except Exception as e:
                self.send_error(502, f"Could not get image: {e}")
        elif self.path == "/shutdown":  # for testing: crash the container
            self.respond(200, "text/plain", b"Shutting down\n")
            print("Shutdown requested", flush=True)
            threading.Thread(target=lambda: os._exit(1)).start()
        else:
            self.send_error(404, "Not Found")


port = int(os.environ.get("PORT", "8080"))
server = HTTPServer(("0.0.0.0", port), TodoHandler)
print(f"Server started in port {port}", flush=True)
server.serve_forever()

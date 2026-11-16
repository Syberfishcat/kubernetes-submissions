import os
import time
import uuid
from datetime import datetime, timezone

LOG_DIR = os.environ.get("LOG_DIR", "/app/logs")
LOG_FILE = os.path.join(LOG_DIR, "log.txt")

random_string = str(uuid.uuid4())


def now():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


os.makedirs(LOG_DIR, exist_ok=True)

while True:
    line = f"{now()}: {random_string}"
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")
    print(line, flush=True)
    time.sleep(5)

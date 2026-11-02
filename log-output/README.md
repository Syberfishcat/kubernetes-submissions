## Log output app

Prints a timestamp and the same randomly generated UUID every 5 seconds.

Run locally: `python3 main.py`

Deploy: `kubectl create deployment log-output --image=sybercat/log-output:1.1`

View logs: `kubectl logs -f deployment/log-output`
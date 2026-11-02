## Log output app

Prints a timestamp and the same randomly generated UUID every 5 seconds.

Run locally: `python3 main.py`

Deploy from the log-output directory:
`kubectl apply -f manifests/deployment.yaml`

View logs:
`kubectl logs -f deployment/log-output`
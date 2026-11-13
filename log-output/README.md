## Log output app

Prints a timestamp and the same randomly generated UUID every 5 seconds.
It also serves the current timestamp and UUID over HTTP at `/` (port 8080 by default, override with the `PORT` env var).

Run locally: `python3 main.py`, then `curl http://localhost:8080/`

Deploy from the log-output directory:
`kubectl apply -f manifests/`

This applies the Deployment, the Service (`log-output-svc`, port 2345 -> container port 8080) and the Ingress (`/` -> `log-output-svc`).

View logs:
`kubectl logs -f deployment/log-output`

Access through the Ingress (with the k3d cluster mapping port 8081 to the load balancer's port 80):
`curl http://localhost:8081/`

## Log output app

One Pod, two containers sharing an `emptyDir` volume at `/app/logs`:

- `log-generator`: writes a timestamp and a random UUID to `log.txt` every 5 seconds.
- `log-reader`: serves the content of `log.txt` over HTTP GET `/` (port 8080).

Deploy from the log-output directory:
`kubectl apply -f manifests/`

View logs:
`kubectl logs -f deployment/log-output -c log-generator`

Access through the Ingress (k3d port 8081 -> 80):
`curl http://localhost:8081/`

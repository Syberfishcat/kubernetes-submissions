## Todo app

A web server that reads the PORT environment variable and
prints "Server started in port NNNN" on startup.
The default port is 8080.

Run locally: `PORT=3000 python3 main.py`

Deploy from the the-project directory:
`kubectl apply -f manifests/deployment.yaml`

View logs:
`kubectl logs -f deployment/todo-app`
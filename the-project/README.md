## Todo app

Returns a simple HTML page at `/`. Uses `PORT` (default: `8080`).

Run commands from `the-project`.

Deploy and access (exposed through a NodePort Service):

```sh
kubectl apply -f manifests/
kubectl rollout status deployment/todo-app
```

The Service maps `localhost:8082` -> NodePort `30080` -> container port `3000`, so open <http://localhost:8082/> in a browser.

The k3d cluster must be created with the port mapping:

```sh
k3d cluster create --port 8082:30080@agent:0 -p 8081:80@loadbalancer --agents 2
```

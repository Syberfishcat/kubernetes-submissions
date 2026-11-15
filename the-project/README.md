## Todo app

Returns a simple HTML page at `/`. Uses `PORT` (default: `8080`).

Run commands from `the-project`.

Deploy and access (exposed through an Ingress):

```sh
kubectl apply -f manifests/
kubectl rollout status deployment/todo-app
```

Traffic flows `localhost:8081` -> Ingress (port `80`) -> ClusterIP Service `todo-app-svc` (port `2345`) -> container port `3000`, so open <http://localhost:8081/> in a browser.

The k3d cluster must be created with the loadbalancer port mapping:

```sh
k3d cluster create -p 8081:80@loadbalancer --agents 2
```

## Todo app

Returns a simple HTML page at `/`. Uses `PORT` (default: `8080`).

Run commands from `the-project`.

Deploy and access:

```sh
kubectl apply -f manifests/deployment.yaml
kubectl rollout status deployment/todo-app
kubectl port-forward deployment/todo-app 8080:3000
```

Keep port-forward running and open <http://localhost:8080/> in a browser.

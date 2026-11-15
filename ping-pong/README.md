## Ping-pong app

Responds with `pong N` to `GET /pingpong` and increments the in-memory counter `N`. Uses `PORT` (default: `3000`).

Deploy (the Ingress is shared with log-output):

```sh
kubectl apply -f manifests/ -f ../log-output/manifests/
curl http://localhost:8081/pingpong
```

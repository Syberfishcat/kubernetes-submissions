## Log output app

One Pod, two containers sharing the `logs-claim` PersistentVolumeClaim at `/app/logs` (also shared with ping-pong):

- `log-generator`: writes a timestamp and a random UUID to `log.txt` every 5 seconds.
- `log-reader`: serves the last line of `log.txt` and the count from `pingpong.txt` on GET `/` (port 8080).

PV and PVC are in [../volumes](../volumes). Create the node directory first, then deploy from the repo root:

```sh
docker exec k3d-k3s-default-agent-0 mkdir -p /tmp/kube
kubectl apply -f volumes/
kubectl apply -f log-output/manifests/ -f ping-pong/manifests/
curl http://localhost:8081/
```

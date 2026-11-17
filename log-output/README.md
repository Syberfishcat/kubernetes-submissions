## Log output app

One Pod, two containers sharing the `logs-claim` PersistentVolumeClaim at `/app/logs` (not used by ping-pong):

- `log-generator`: writes a timestamp and a random UUID to `log.txt` every 5 seconds.
- `log-reader`: serves the last line of `log.txt` and the number of pongs (fetched over HTTP from ping-pong `GET /pings`) on GET `/` (port 8080).

PV and PVC are in [../volumes/logs-pv.yaml](../volumes/logs-pv.yaml) and [../volumes/logs-pvc.yaml](../volumes/logs-pvc.yaml). Create the node directory first, then deploy from the repo root:

```sh
docker exec k3d-k3s-default-agent-0 mkdir -p /tmp/kube
kubectl apply -f volumes/logs-pv.yaml -f volumes/logs-pvc.yaml
kubectl apply -f log-output/manifests/ -f ping-pong/manifests/
curl http://localhost:8081/
```

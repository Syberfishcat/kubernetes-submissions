## Todo app

Shows a random picture from Picsum at `/`. The image is cached in a PersistentVolume (`/app/images`) and refreshed every 10 minutes.
Uses `PORT` (default: `8080`). `GET /shutdown` crashes the container for testing.

Run commands from `the-project`.

```sh
k3d cluster create -p 8081:80@loadbalancer --agents 2
docker exec k3d-k3s-default-agent-0 mkdir -p /tmp/kube
kubectl apply -f ../volumes/project-pv.yaml -f ../volumes/project-pvc.yaml
kubectl apply -f manifests/
```

Open <http://localhost:8081/> (`localhost:8081` -> Ingress -> Service `2345` -> container `3000`).

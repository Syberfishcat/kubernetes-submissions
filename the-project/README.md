## Todo app

Shows a random Picsum image (cached in a PersistentVolume), a todo input (max 140 chars), a Send button and a hardcoded todo list.

Run commands from `the-project`.

```sh
k3d cluster create -p 8081:80@loadbalancer --agents 2
docker exec k3d-k3s-default-agent-0 mkdir -p /tmp/kube
kubectl apply -f ../volumes/project-pv.yaml -f ../volumes/project-pvc.yaml
kubectl apply -f manifests/
```

Open <http://localhost:8081/>.

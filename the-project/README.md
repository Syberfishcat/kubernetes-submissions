## Todo app

Runs in the `project` namespace. Two services behind one Ingress:

- `todo-app/` (frontend): serves `index.html`, `script.js` and a random Picsum image (cached in a PersistentVolume). The page has a todo input (max length from config), a Send button and the todo list.
- `todo-backend/`: `GET /todos` returns the todos, `POST /todos` creates one. Todos are kept in memory.

The Ingress routes `/todos` to `todo-backend-svc` and everything else to `todo-app-svc`, so the browser talks to the backend directly.

All configuration (port, image URL, cache time, max todo length) comes from env variables set in the deployments and [manifests/configmap.yaml](manifests/configmap.yaml).

Run commands from `the-project`.

```sh
k3d cluster create -p 8081:80@loadbalancer --agents 2
docker exec k3d-k3s-default-agent-0 mkdir -p /tmp/kube
kubectl apply -f manifests/namespace.yaml
kubectl apply -f ../volumes/project-pv.yaml -f ../volumes/project-pvc.yaml
kubectl apply -f manifests/
```

Open <http://localhost:8081/>.

## Todo app

Two services behind one Ingress:

- `todo-app/` (frontend): serves `index.html`, `script.js` and a random Picsum image (cached in a PersistentVolume). The page has a todo input (max 140 characters), a Send button and the todo list.
- `todo-backend/`: `GET /todos` returns the todos, `POST /todos` creates one. Todos are kept in memory.

The Ingress routes `/todos` to `todo-backend-svc` and everything else to `todo-app-svc`, so the browser talks to the backend directly.

Run commands from `the-project`.

```sh
docker build -t sybercat/todo-app:2.2 todo-app
docker build -t sybercat/todo-backend:2.2 todo-backend
docker push sybercat/todo-app:2.2
docker push sybercat/todo-backend:2.2

k3d cluster create -p 8081:80@loadbalancer --agents 2
docker exec k3d-k3s-default-agent-0 mkdir -p /tmp/kube
kubectl apply -f ../volumes/project-pv.yaml -f ../volumes/project-pvc.yaml
kubectl apply -f manifests/
```

Open <http://localhost:8081/>.

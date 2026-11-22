## Todo app

Runs in the `project` namespace:

- `todo-app`: frontend with the todo list and a random image.
- `todo-backend`: `GET /todos` and `POST /todos`. Todos are stored in Postgres.
- `postgres-ss`: Postgres StatefulSet with one replica. The backend reads `DATABASE_URL` from [postgres-secret.yaml](manifests/postgres-secret.yaml), other settings from [configmap.yaml](manifests/configmap.yaml).
- `random-wiki-todo`: [CronJob](manifests/todo-cronjob.yaml) that adds a `Read <random Wikipedia URL>` todo every hour.

Run from `the-project`:

```sh
k3d cluster create -p 8081:80@loadbalancer --agents 2
docker exec k3d-k3s-default-agent-0 mkdir -p /tmp/kube
kubectl apply -f manifests/namespace.yaml
kubectl apply -f ../volumes/project-pv.yaml -f ../volumes/project-pvc.yaml
kubectl apply -f manifests/
```

Open <http://localhost:8081/>.

To run the CronJob right away:

```sh
kubectl -n project create job --from=cronjob/random-wiki-todo wiki-now
```

## Todo app

Runs in the `project` namespace:

- `todo-app`: frontend with the todo list and a random image.
- `todo-backend`: `GET /todos` and `POST /todos`. Todos are stored in Postgres. Todos over 140 characters are rejected.
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

## Logging

Backend logs every posted todo (`Created todo` / `Rejected todo`). Logs go to Loki and are viewed in Grafana:

```sh
helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack -n prometheus --create-namespace
helm install loki grafana/loki-stack -n loki-stack --create-namespace
kubectl -n prometheus port-forward svc/kube-prometheus-stack-grafana 3000:80
```

In Grafana, add Loki (`http://loki.loki-stack.svc.cluster.local:3100`) and query:

```logql
{namespace="project", app="todo-backend"} |= "Rejected"
```

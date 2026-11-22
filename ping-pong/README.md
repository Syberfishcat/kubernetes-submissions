## Ping-pong app

Responds with `pong N` to `GET /pingpong`. `GET /pings` returns the current count (used by the log-output app). Uses `PORT` (default: `3000`).

The counter is stored in Postgres, which runs as a StatefulSet with one replica ([postgres-statefulset.yaml](manifests/postgres-statefulset.yaml)). Its data lives in a PVC created from `volumeClaimTemplates`. `DATABASE_URL` and the password come from [postgres-secret.yaml](manifests/postgres-secret.yaml). On startup the app retries until the database accepts connections, then creates the `counter` table if it doesn't exist.

Deploy as described in the [log-output README](../log-output/README.md). To check the database:

```sh
kubectl -n exercises run psql-for-debugging -it --rm --restart=Never --image postgres:16 -- \
  psql postgres://postgres:example@postgres-svc:5432/postgres -c 'select * from counter;'
```

## Todo app

A web server that reads the PORT environment variable and
prints "Server started in port NNNN" on startup.
The default port is 8080.

Run locally: `PORT=3000 python3 main.py`

First deployment:
`kubectl create deployment todo-app --image=sybercat/todo-app:1.2`

Set the port:
`kubectl set env deployment/todo-app PORT=3000`

View logs:
`kubectl logs -f deployment/todo-app`
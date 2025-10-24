messaging_app

Purpose
-------
This README contains quick commands to run the Django `messaging_app` locally using Docker Compose and verification steps for the ALX project and the Kubernetes helper scripts included in this repository.

Prerequisites
-------------
- Docker (and docker-compose plugin)
- Python 3.10 (for local dev without docker)
- Minikube and kubectl (for Kubernetes tasks)

Environment
-----------
Copy the example env and edit secrets before starting:

```bash
cp .env.example .env
# open .env and set MYSQL_DB, MYSQL_USER, MYSQL_PASSWORD, MYSQL_ROOT_PASSWORD
```

Run with Docker Compose (recommended)
------------------------------------
Build and run the services (web + mysql):

```bash
# build and run in foreground (use ctrl-c to stop)
docker compose up --build

# or run in background (detached)
docker compose up --build -d
```

If you need a fresh DB initialization:

```bash
# stop and remove containers and volumes (this will delete DB data)
docker compose down -v
```

Check logs and server

```bash
# follow web logs
docker compose logs -f web

# check HTTP response from Django dev server (should be reachable on port 8000)
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000
```

Run Django management commands inside the container

```bash
# run migrations
docker compose run --rm web python manage.py migrate --noinput

# run tests
docker compose run --rm web python manage.py test
```

Notes about expected HTTP status
- The ALX autograder expects the Django server to be listening on port 8000. A 200, 301 or 404 response from the curl check above indicates the server responded and is listening. If you see no response or a connection refused error, the server didn't start.

Kubernetes (Minikube) quick-start
---------------------------------
These scripts and manifests are provided for the Kubernetes tasks. Example workflow to run locally:

```bash
# start minikube with docker driver
minikube start --driver=docker

# (optional) build image inside minikube's docker env
eval $(minikube -p minikube docker-env)
docker build -t messaging-app:1.0 .
# or load the image into minikube
minikube image load messaging-app:1.0

# apply manifests
kubectl apply -f deployment.yaml
kubectl apply -f kubeservice.yaml
kubectl apply -f ingress.yaml

# get service URL
minikube service messaging-app-service --url

# when finished
minikube stop
```

Files and scripts of interest
-----------------------------
- `Dockerfile` — builds the Django web image (Python 3.10-slim). Uses `requirements.txt`.
- `docker-compose.yml` — orchestrates `web` and `db` (MySQL) using `.env`
- `.env.example` — template for required DB env variables
- `kubctl-0x01`, `kubctl-0x-02`, `kubctl-0x-03`, `kurbeScript` — helper scripts for the ALX Kubernetes tasks
- `deployment.yaml`, `blue_deployment.yaml`, `green_deployment.yaml`, `kubeservice.yaml`, `ingress.yaml` — Kubernetes manifests
- `docs/minikube_k8s_troubleshooting.md` — troubleshooting guide for common minikube/docker/k8s issues on Debian-based systems

Pre-push checklist (run before pushing to GitHub)
-------------------------------------------------
1. Confirm `.env` exists and contains correct DB creds (do NOT commit `.env`)
2. Run tests:

```bash
docker compose run --rm web python manage.py test
```

3. Run a smoke test:

```bash
# start in background
docker compose up --build -d
# wait 5-10s
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000
```

Acceptable: any numeric HTTP response code (means server reachable). If you prefer check for 200 specifically, modify the curl command.

4. (Optional) If you edited requirements, ensure no build errors in Docker image by running `docker compose build`.

How I tested / deployment status
-------------------------------
I cannot directly deploy to your personal PC from this environment. I created and updated files inside the repository (added `README.md` and `docs/minikube_k8s_troubleshooting.md`, plus `kubctl-0x03`) and verified file permissions for helper scripts. To fully confirm runtime behavior (Docker Compose startup, DB initialization, Django responds on port 8000, and Minikube manifests apply cleanly) you should run the commands above on your machine and paste the outputs here if you'd like me to validate them.

If you want me to try running the Docker Compose and Kubernetes commands here (in this workspace), say so and I will attempt to run them and report back. Note: deploying requires Docker and/or Minikube to be available and running in this environment; if they are not present I'll report the exact error and provide remediation steps.

Contact / next steps
--------------------
- Run the pre-push checklist locally and paste the outputs if you want me to inspect them.
- Or allow me to run the verification commands in this environment and I'll try them now and report results.

End of README snippet

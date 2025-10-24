# alx-backend-python

This repository contains several backend-focused projects and exercises used for learning and demonstration. The primary subproject for this CI/CD task is the `messaging_app` Django application.

Key CI/CD files (added)

- `.github/workflows/ci.yml` — GitHub Actions workflow that runs tests, linting, and uploads reports.
- `.github/workflows/dep.yml` — GitHub Actions workflow that builds and pushes a Docker image to Docker Hub on `main`.
- `messaging_app/Jenkinsfile` — Jenkins pipeline to run tests, build a Docker image, and push to Docker Hub.

Quick start (local)

1. Install dev dependencies (recommended inside a virtualenv):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate; python -m pip install --upgrade pip; python -m pip install -r requirements-dev.txt
```

2. Run tests locally:

```powershell
python -m pytest -q
```

3. Start Jenkins (optional):

```powershell
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
```

Notes

- Move or confirm GitHub Actions workflows are in `.github/workflows` at the repository root so Actions can run on push.
- Add the GitHub Secrets `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` to enable image push from Actions.
- Add Jenkins credentials `docker-hub-creds` and `github-creds` to enable Jenkins pipeline push and checkout.

If you want me to push these changes to GitHub for you, I can attempt a push now — it may require your Git credentials.

# alx-backend-python

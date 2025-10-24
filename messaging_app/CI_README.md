# CI / CD Integration Notes for messaging_app

This file documents how Jenkins and GitHub Actions have been wired for the `messaging_app` project.

Files added

- `messaging_app/Jenkinsfile` — Jenkins pipeline that checks out code, prepares a Python venv, runs tests with `pytest`, builds a Docker image, and (on the `main` branch) pushes to Docker Hub. It expects a Jenkins credential with id `docker-hub-creds` (username/password).
- `messaging_app/.github/workflows/ci.yml` — GitHub Actions workflow that runs on push and pull requests, installs dependencies, runs `flake8`, runs tests with coverage, and uploads artifacts.
- `messaging_app/.github/workflows/dep.yml` — GitHub Actions workflow that builds and pushes Docker images to Docker Hub when commits are pushed to `main`. Requires GitHub Secrets `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN`.

Quick setup

1. Jenkins

   - Start Jenkins (recommended in Docker):

     docker run -d --name jenkins -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts

   - Install recommended plugins: Git, Pipeline, Docker Pipeline (or ShiningPanda if you want Python virtualenv integration).
   - Add credentials:
     - `github-creds` (GitHub personal access token) for repo checkout if needed.
     - `docker-hub-creds` (username/password) for docker login.
   - Create a pipeline job pointing to this repository (or create a Multibranch Pipeline). The `Jenkinsfile` at `messaging_app/Jenkinsfile` will run the pipeline.

2. GitHub Actions
   - Add repository secrets:
     - `DOCKERHUB_USERNAME` — your Docker Hub username
     - `DOCKERHUB_TOKEN` — a Docker Hub access token or password
   - CI workflow will run on push and PRs. The MySQL service is configured for tests that require it.

Notes & manual QA request

- Tests: Workflows assume `messaging_app/requirements.txt` exists. If your tests have other requirements, add them there.
- Adjust Docker image name (`DOCKERHUB_REPO`) in `messaging_app/Jenkinsfile`.
- After you've reviewed these files, please run the Jenkins pipeline manually and the GitHub Actions workflows by pushing a test branch/PR. When ready, request a manual QA review for final verification.

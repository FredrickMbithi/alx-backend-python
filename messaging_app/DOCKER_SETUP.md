# Docker Deployment Setup

This workflow (`dep.yml`) automatically builds and pushes a Docker image to Docker Hub when changes are pushed to the `main` branch.

## Prerequisites

You need to configure GitHub Secrets for Docker Hub authentication:

### Setting up GitHub Secrets

1. Go to your GitHub repository: `https://github.com/FredrickMbithi/alx-backend-python`
2. Click on **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add the following secrets:

   - **DOCKER_USERNAME**: Your Docker Hub username
   - **DOCKER_PASSWORD**: Your Docker Hub password or access token

### Docker Hub Access Token (Recommended)

Instead of using your Docker Hub password, it's recommended to use an access token:

1. Log in to [Docker Hub](https://hub.docker.com/)
2. Go to **Account Settings** → **Security** → **New Access Token**
3. Create a token with **Read, Write, Delete** permissions
4. Copy the token and use it as `DOCKER_PASSWORD` in GitHub Secrets

## Workflow Features

- ✅ Builds Docker image on push to `main` branch
- ✅ Pushes image to Docker Hub as `<username>/messaging_app`
- ✅ Tags images with:
  - `latest` (for main branch)
  - Branch name
  - Git commit SHA
- ✅ Uses Docker layer caching for faster builds
- ✅ Secure credential management via GitHub Secrets

## Manual Trigger

You can also manually trigger the workflow:

1. Go to **Actions** tab in your repository
2. Select **Docker Build and Push** workflow
3. Click **Run workflow**

## Image Location

After the workflow runs successfully, your Docker image will be available at:

```
docker pull <your-docker-username>/messaging_app:latest
```

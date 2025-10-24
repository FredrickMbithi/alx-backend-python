# GitHub Actions CI/CD Setup

This directory contains GitHub Actions workflows for the messaging app.

## Workflows

### 1. CI - Testing and Code Quality (`ci.yml`)

**Triggers:**

- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`

**Jobs:**

#### Test Job

- Sets up MySQL 8.0 service
- Installs Python 3.10 and system dependencies
- Runs Django migrations
- Executes pytest with coverage
- Uploads test results and coverage reports as artifacts

#### Lint Job

- Runs flake8 for code quality checks
- Checks for syntax errors and critical issues
- Generates linting statistics

#### Summary Job

- Provides build status summary
- Fails if any job fails

**Artifacts Generated:**

- `test-results.xml` - JUnit test results
- `coverage-report-html` - HTML coverage report
- `coverage-report-xml` - XML coverage report

---

### 2. Deploy - Docker Image (`dep.yml`)

**Triggers:**

- Push to `main` branch
- Version tags (`v*`)
- Manual workflow dispatch

**Steps:**

1. Checkout code
2. Login to Docker Hub using secrets
3. Extract metadata and generate tags
4. Build Docker image with Buildx
5. Push image to Docker Hub
6. Inspect and verify image

**Docker Tags Generated:**

- `latest` - Latest main branch build
- `<branch-name>` - Branch-specific tag
- `<sha>` - Commit SHA tag
- `v1.0.0` - Semantic version tags

---

## Required GitHub Secrets

To use these workflows, configure the following secrets in your GitHub repository:

### For Docker Deployment (dep.yml)

1. Go to: **Settings** → **Secrets and variables** → **Actions**
2. Add the following secrets:

| Secret Name       | Description                  | Example          |
| ----------------- | ---------------------------- | ---------------- |
| `DOCKER_USERNAME` | Your Docker Hub username     | `yourusername`   |
| `DOCKER_PASSWORD` | Your Docker Hub access token | `dckr_pat_xxxxx` |

**How to create Docker Hub access token:**

1. Go to https://hub.docker.com/settings/security
2. Click **New Access Token**
3. Give it a name (e.g., "GitHub Actions")
4. Copy the token and save it as `DOCKER_PASSWORD` secret

---

## Local Testing

### Test CI workflow locally

```bash
# Install dependencies
cd messaging_app
pip install -r requirements.txt
pip install pytest pytest-django pytest-cov flake8

# Run tests
pytest chats/ --cov=chats --cov-report=html

# Run linting
flake8 . --exclude=venv,migrations,__pycache__
```

### Test Docker build locally

```bash
cd messaging_app
docker build -t messaging-app:local .
docker run -d -p 8000:8000 messaging-app:local
```

---

## Viewing Results

### Test Results

1. Go to **Actions** tab in GitHub
2. Click on a workflow run
3. Download artifacts:
   - `test-results` - JUnit XML
   - `coverage-report-html` - Browse coverage in browser
   - `coverage-report-xml` - For CI tools integration

### Docker Images

1. Visit your Docker Hub repository: `https://hub.docker.com/r/<username>/messaging-app`
2. View available tags and pull statistics

---

## Workflow Status Badges

Add these to your README.md:

```markdown
![CI Tests](https://github.com/FredrickMbithi/alx-backend-python/workflows/CI%20-%20Testing%20and%20Code%20Quality/badge.svg)
![Docker Deploy](https://github.com/FredrickMbithi/alx-backend-python/workflows/Deploy%20-%20Build%20and%20Push%20Docker%20Image/badge.svg)
```

---

## Troubleshooting

### MySQL Connection Issues

- Ensure health check is passing before migrations
- Verify `DATABASE_HOST` is set to `127.0.0.1`

### Docker Push Failures

- Verify `DOCKER_USERNAME` and `DOCKER_PASSWORD` secrets are set correctly
- Check Docker Hub access token has write permissions
- Ensure repository exists on Docker Hub (or set it to auto-create)

### Flake8 Failures

- Review the linting output in workflow logs
- Fix critical errors (E9, F63, F7, F82)
- Warnings won't fail the build but should be addressed

---

## Best Practices

✅ **Keep dependencies updated** - Regularly update `requirements.txt`  
✅ **Write tests** - Maintain high test coverage (>80%)  
✅ **Follow PEP 8** - Use flake8 recommendations  
✅ **Use semantic versioning** - Tag releases as `v1.0.0`, `v1.1.0`, etc.  
✅ **Review artifacts** - Check coverage reports after each run  
✅ **Monitor Docker image size** - Keep images optimized

---

**Author:** Fredrick Mbithi  
**Project:** ALX Backend Python - Messaging App  
**Date:** October 2025

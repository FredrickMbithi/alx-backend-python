# Jenkins CI/CD Setup for Django Messaging App

This directory contains a complete CI/CD setup using Jenkins, Docker, and MySQL for the Django messaging application.

## 📁 Files Overview

- **Jenkinsfile** - Production-ready pipeline for building, testing, and deploying the Django app
- **docker-compose-ci.yml** - Complete Docker Compose stack with Jenkins, MySQL databases, and Django app
- **Dockerfile** - Container image for the Django application
- **requirements.txt** - Python dependencies

## 🚀 Quick Start

### 1. Start the CI/CD Stack

```bash
cd messaging_app

# Start all services (Jenkins + MySQL + Django)
docker-compose -f docker-compose-ci.yml up -d

# View logs
docker-compose -f docker-compose-ci.yml logs -f
```

### 2. Access Jenkins

1. Open browser: `http://localhost:8080`
2. Get initial admin password:
   ```bash
   docker exec jenkins-server cat /var/jenkins_home/secrets/initialAdminPassword
   ```
3. Complete Jenkins setup wizard
4. Install recommended plugins + these additional plugins:
   - **Git Plugin**
   - **GitHub Plugin**
   - **Pipeline Plugin**
   - **JUnit Plugin**
   - **Docker Pipeline Plugin**

### 3. Configure Jenkins Credentials

**GitHub Access:**

1. Go to Jenkins → Manage Jenkins → Manage Credentials
2. Add credentials:
   - **Kind:** Username with password
   - **ID:** `github-creds`
   - **Username:** Your GitHub username
   - **Password:** Your GitHub Personal Access Token
   - **Description:** GitHub Access Token

### 4. Create Jenkins Pipeline Job

1. Click **New Item**
2. Name: `messaging-app-pipeline`
3. Type: **Pipeline**
4. Under **Pipeline** section:
   - **Definition:** Pipeline script from SCM
   - **SCM:** Git
   - **Repository URL:** `https://github.com/FredrickMbithi/alx-backend-python.git`
   - **Credentials:** Select `github-creds`
   - **Branch:** `*/main`
   - **Script Path:** `messaging_app/Jenkinsfile`
5. Save and click **Build Now**

## 🐳 Docker Services

### Jenkins Server

- **URL:** http://localhost:8080
- **Container:** `jenkins-server`
- **Image:** `jenkins/jenkins:lts`
- **Purpose:** CI/CD orchestration and automation

### MySQL for CI (Testing)

- **Port:** 3307 (host) → 3306 (container)
- **Container:** `mysql-ci`
- **Database:** `messaging_db`
- **User:** `messaging_user`
- **Password:** `password`
- **Purpose:** Database for Jenkins pipeline tests

### MySQL for Django App

- **Port:** 3306
- **Container:** `mysql-app`
- **Database:** `messaging_db`
- **User:** `messaging_user`
- **Password:** `password`
- **Purpose:** Database for local Django development

### Django Application

- **URL:** http://localhost:8000
- **Container:** `django-messaging-app`
- **Purpose:** Local development and testing

## 📋 Pipeline Stages

The Jenkinsfile defines these stages:

1. **Checkout** - Clone code from GitHub
2. **Install System Dependencies** - Install OS packages for mysqlclient (gcc, python3-dev, MySQL headers)
3. **Setup Python Environment** - Create virtual environment in `messaging_app/`
4. **Install Python Dependencies** - Install from requirements.txt + verify mysqlclient
5. **Start MySQL Container** - Spin up test database if Docker is available
6. **Run Database Migrations** - Apply Django migrations
7. **Run Tests** - Execute pytest with JUnit XML report
8. **Post Actions** - Publish test results, cleanup, notify

## 🔧 Pipeline Features

✅ **Automatic subfolder navigation** - All commands run inside `messaging_app/`  
✅ **OS dependency management** - Installs system packages for mysqlclient build  
✅ **MySQL integration** - Starts test database container automatically  
✅ **Environment isolation** - Creates Python venv per build  
✅ **Test reporting** - Publishes JUnit XML results to Jenkins  
✅ **Clean workspace** - Removes venv and cache after build  
✅ **Clear logging** - Emoji-rich status messages for easy debugging  
✅ **Error handling** - Fails fast with descriptive error messages

## 🧪 Running Tests Locally

### Using Docker Compose

```bash
# Run tests in the Django container
docker-compose -f docker-compose-ci.yml run --rm django-app sh -c \
  "pytest . --junitxml=report.xml --verbose"
```

### Using Local Python

```bash
cd messaging_app

# Create venv
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set Django settings
export DJANGO_SETTINGS_MODULE=messaging_app.settings

# Set database connection (if using Docker MySQL)
export DATABASE_HOST=127.0.0.1
export DATABASE_PORT=3306
export DATABASE_NAME=messaging_db
export DATABASE_USER=messaging_user
export DATABASE_PASSWORD=password

# Run migrations
python manage.py migrate

# Run tests
pytest . --junitxml=report.xml --verbose
```

## 🛠️ Troubleshooting

### Jenkins Can't Access Docker

**Issue:** Pipeline fails at "Start MySQL Container" stage

**Solution:**

```bash
# Ensure Docker socket is accessible
docker exec -u root jenkins-server chmod 666 /var/run/docker.sock

# Install Docker CLI in Jenkins container
docker exec -u root jenkins-server sh -c \
  "apt-get update && apt-get install -y docker.io"
```

### mysqlclient Build Fails

**Issue:** `error: mysql.h: No such file or directory`

**Solution:** The "Install System Dependencies" stage should handle this automatically. If it fails:

```bash
# SSH into Jenkins container
docker exec -it jenkins-server bash

# Install manually
apt-get update
apt-get install -y build-essential gcc python3-dev pkg-config default-libmysqlclient-dev
```

### Database Connection Refused

**Issue:** Tests fail with "Can't connect to MySQL server"

**Solution:**

```bash
# Check MySQL is running
docker ps | grep mysql-ci

# Check MySQL health
docker inspect mysql-ci | grep -A 5 Health

# Verify database exists
docker exec -it mysql-ci mysql -u messaging_user -ppassword -e "SHOW DATABASES;"
```

### Tests Not Found

**Issue:** `ERROR: not found: /var/jenkins_home/workspace/.../tests`

**Solution:** Ensure:

- The `dir('messaging_app')` wraps all test commands in Jenkinsfile
- Tests are in `messaging_app/chats/tests.py` or similar Django app structure
- `DJANGO_SETTINGS_MODULE` is set correctly

## 📦 Updating Dependencies

To add new Python packages:

1. Update `requirements.txt`
2. Commit and push to GitHub
3. Jenkins will automatically install new dependencies on next build

## 🔒 Production Considerations

Before deploying to production:

- [ ] Replace hardcoded passwords with Jenkins credentials/secrets
- [ ] Use environment-specific settings files
- [ ] Add stages for: linting (flake8/black), security scanning (bandit), Docker image build/push
- [ ] Configure Jenkins backup strategy
- [ ] Set up branch protection and PR-based testing
- [ ] Add Slack/email notifications on build failure
- [ ] Use persistent volumes for Jenkins workspace
- [ ] Enable HTTPS for Jenkins (reverse proxy with Nginx/Traefik)

## 📚 Additional Resources

- [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [pytest-django Documentation](https://pytest-django.readthedocs.io/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Django Testing Guide](https://docs.djangoproject.com/en/stable/topics/testing/)

## 📝 Notes

- Jenkins workspace is mapped read-only to avoid accidental modifications
- MySQL CI database uses port 3307 to avoid conflicts with local MySQL
- All pipeline stages use `sh` (Unix/Linux) - Windows agents not supported
- Test database is recreated on each build for clean state
- Virtual environment is cleaned up after each build to save disk space

---

**Author:** Fredrick Mbithi  
**Project:** ALX Backend Python - Messaging App  
**Date:** October 2025

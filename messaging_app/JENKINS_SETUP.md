# Jenkins Setup Guide for messaging_app

## Step 1: Install and Run Jenkins in Docker

Run Jenkins in a Docker container:

```bash
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
```

This command:

- **Pulls** the latest LTS Jenkins image
- **Exposes** Jenkins on port 8080 (web UI) and 50000 (agent communication)
- **Persists** data using a named volume `jenkins_home`
- **Runs** Jenkins in detached mode

### Check Jenkins is Running

```bash
docker ps | grep jenkins
docker logs jenkins
```

## Step 2: Access Jenkins Dashboard

1. Open your browser and go to: **http://localhost:8080**

2. Get the initial admin password:

   ```bash
   docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
   ```

3. Copy the password and paste it into the Jenkins setup wizard

4. Select **"Install suggested plugins"**

5. Create your first admin user account

## Step 3: Install Required Plugins

### Method 1: Via Jenkins UI

1. Go to **Manage Jenkins** → **Manage Plugins**
2. Click on the **"Available"** tab
3. Search and install these plugins:

   - **Git plugin** (for GitHub integration)
   - **Pipeline** (for Jenkinsfile support)
   - **ShiningPanda Plugin** (for Python/virtualenv support)
   - **HTML Publisher Plugin** (for HTML reports)
   - **JUnit Plugin** (for test reports)
   - **Cobertura Plugin** or **Coverage Plugin** (for coverage reports)

4. Check **"Restart Jenkins when installation is complete"**

### Method 2: Via Jenkins CLI (Alternative)

```bash
docker exec jenkins jenkins-plugin-cli --plugins \
  git \
  workflow-aggregator \
  shiningpanda \
  htmlpublisher \
  junit \
  cobertura
```

## Step 4: Configure Python in Jenkins

### Install Python in Jenkins Container

```bash
# Access Jenkins container
docker exec -it jenkins bash

# Install Python (as root)
apt-get update
apt-get install -y python3 python3-pip python3-venv

# Verify installation
python3 --version
pip3 --version

# Exit container
exit
```

### Alternative: Use Python Tool Configuration

1. Go to **Manage Jenkins** → **Global Tool Configuration**
2. Scroll to **ShiningPanda**
3. Add a Python installation:
   - Name: `Python-3.10`
   - Install automatically: ✅
   - Or specify path: `/usr/bin/python3`

## Step 5: Add GitHub Credentials

### Create GitHub Personal Access Token (PAT)

1. Go to GitHub: **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
2. Click **"Generate new token (classic)"**
3. Give it a name: `jenkins-access`
4. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `admin:repo_hook` (if using webhooks)
5. Click **"Generate token"**
6. **Copy the token** (you won't see it again!)

### Add Credentials to Jenkins

1. Go to **Manage Jenkins** → **Manage Credentials**
2. Click on **(global)** domain
3. Click **"Add Credentials"**
4. Fill in:
   - **Kind**: Username with password
   - **Scope**: Global
   - **Username**: Your GitHub username (e.g., `FredrickMbithi`)
   - **Password**: Paste your Personal Access Token
   - **ID**: `github-credentials`
   - **Description**: GitHub Access Token
5. Click **"Create"**

## Step 6: Create Jenkins Pipeline Job

### Create New Pipeline

1. From Jenkins dashboard, click **"New Item"**
2. Enter name: `messaging_app_pipeline`
3. Select **"Pipeline"**
4. Click **"OK"**

### Configure Pipeline

#### General Settings

- ✅ **Discard old builds**
  - Days to keep: `7`
  - Max # of builds: `10`

#### Build Triggers (Optional)

- ✅ **Poll SCM**: `H/5 * * * *` (every 5 minutes)
- Or ✅ **GitHub hook trigger for GITScm polling** (for webhooks)

#### Pipeline Configuration

**Definition**: Pipeline script from SCM

**SCM**: Git

**Repository URL**: `https://github.com/FredrickMbithi/alx-backend-python.git`

**Credentials**: Select `github-credentials`

**Branch Specifier**: `*/main`

**Script Path**: `messaging_app/Jenkinsfile`

Click **"Save"**

## Step 7: Run the Pipeline

### Manual Trigger

1. From the pipeline job page, click **"Build Now"**
2. Watch the build progress in **"Build History"**
3. Click on the build number (e.g., `#1`)
4. View:
   - **Console Output** - Full logs
   - **Test Result** - JUnit test results
   - **Pytest HTML Report** - Detailed test report
   - **Coverage Report** - Code coverage analysis

### Expected Pipeline Stages

1. ✅ **Checkout** - Pulls code from GitHub
2. ✅ **Setup Python Environment** - Installs dependencies
3. ✅ **Run Tests** - Executes pytest
4. ✅ **Generate Test Report** - Creates JUnit XML and HTML reports

## Step 8: View Test Reports

After a successful build:

### JUnit Test Results

- Click on **"Test Result"** link
- View test summary, passed/failed tests
- Drill down to individual test details

### HTML Reports

- Click on **"Pytest HTML Report"** link
- View detailed test execution report
- Click on **"Coverage Report"** link
- View code coverage metrics

### Artifacts

- Click on **"Build Artifacts"** link
- Download reports:
  - `reports/junit.xml`
  - `reports/report.html`
  - `reports/coverage.xml`
  - `reports/htmlcov/`

## Troubleshooting

### Jenkins Container Not Starting

```bash
# Check container logs
docker logs jenkins

# Restart container
docker restart jenkins

# Remove and recreate
docker rm -f jenkins
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
```

### Python Not Found

```bash
# Install Python in Jenkins container
docker exec -u root jenkins apt-get update
docker exec -u root jenkins apt-get install -y python3 python3-pip

# Verify
docker exec jenkins python3 --version
```

### Plugin Installation Failed

1. Go to **Manage Jenkins** → **Manage Plugins**
2. Click **"Advanced"** tab
3. Click **"Check now"** to update plugin metadata
4. Retry installation

### GitHub Authentication Failed

1. Verify Personal Access Token is valid
2. Check token has `repo` scope
3. Verify credentials ID matches Jenkinsfile (`github-credentials`)
4. Try using SSH instead of HTTPS:
   - Generate SSH key in Jenkins container
   - Add public key to GitHub
   - Update repository URL to SSH format

### Tests Failing

```bash
# Run tests locally first
cd messaging_app
python3 -m pytest -v

# Check requirements.txt is complete
pip3 install -r requirements.txt

# Verify database is accessible (if tests need it)
```

### Reports Not Generating

1. Verify HTML Publisher plugin is installed
2. Check reports directory exists: `messaging_app/reports/`
3. Verify pytest generates files:
   ```bash
   ls -la messaging_app/reports/
   ```
4. Check Console Output for pytest errors

## Verification Checklist

- ✅ Jenkins running at http://localhost:8080
- ✅ Git plugin installed
- ✅ Pipeline plugin installed
- ✅ ShiningPanda plugin installed
- ✅ HTML Publisher plugin installed
- ✅ GitHub credentials added (ID: `github-credentials`)
- ✅ Pipeline job created (`messaging_app_pipeline`)
- ✅ Jenkinsfile exists at `messaging_app/Jenkinsfile`
- ✅ Pipeline runs successfully
- ✅ Test reports generated and visible

## Next Steps

1. **Set up webhooks** (optional):

   - Go to GitHub repository → Settings → Webhooks
   - Add webhook: `http://YOUR_JENKINS_URL/github-webhook/`
   - Payload URL format: `http://<your-ip>:8080/github-webhook/`
   - Content type: `application/json`
   - Events: `Just the push event`

2. **Add email notifications** (optional):

   - Configure SMTP in Jenkins
   - Add post-build action to send emails

3. **Set up multi-branch pipeline** (optional):

   - Create multi-branch pipeline
   - Auto-discover branches with Jenkinsfile

4. **Integrate with SonarQube** (optional):
   - Add code quality analysis

## Useful Commands

```bash
# View Jenkins logs
docker logs -f jenkins

# Access Jenkins container
docker exec -it jenkins bash

# Stop Jenkins
docker stop jenkins

# Start Jenkins
docker start jenkins

# View Jenkins home directory
docker exec jenkins ls -la /var/jenkins_home

# Backup Jenkins home
docker run --rm --volumes-from jenkins -v $(pwd):/backup ubuntu tar cvf /backup/jenkins-backup.tar /var/jenkins_home
```

## References

- [Jenkins Official Documentation](https://www.jenkins.io/doc/)
- [Pipeline Syntax Reference](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [pytest Documentation](https://docs.pytest.org/)
- [ShiningPanda Plugin](https://plugins.jenkins.io/shiningpanda/)

# 🚀 Kubernetes Deployment Tutorial - Django Messaging App

A comprehensive hands-on tutorial for learning Kubernetes deployment strategies using a Django messaging application.

## 📚 Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Tasks Breakdown](#tasks-breakdown)
- [Learning Objectives](#learning-objectives)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

This project demonstrates **production-ready Kubernetes deployment strategies** using a real Django application. You'll learn:
- Container orchestration with Kubernetes
- Scaling applications horizontally
- Zero-downtime deployments
- Load balancing and external access
- Blue-green deployment strategy
- Rolling updates

## 🛠️ Prerequisites

Before starting, ensure you have these installed:

### Required Tools
```bash
# Docker - Containerization platform
docker --version  # Should be 20.10+

# Minikube - Local Kubernetes cluster
minikube version  # Should be v1.25+

# kubectl - Kubernetes CLI
kubectl version --client  # Should be v1.23+

# Python - For Django app
python --version  # Should be 3.8+
```

### Installation Guides

**Windows:**
```powershell
# Install Docker Desktop
# Download from: https://www.docker.com/products/docker-desktop

# Install Minikube
choco install minikube

# Install kubectl
choco install kubernetes-cli
```

**macOS:**
```bash
# Install using Homebrew
brew install docker minikube kubectl
```

**Linux:**
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

## 📂 Project Structure

```
messaging_app/
├── 📄 Django App Files
│   ├── manage.py              # Django project manager
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile             # Container image definition
│   └── docker-compose.yml     # Local development setup
│
├── 📦 Task 0: Cluster Setup
│   ├── kurbeScript           # Starts Minikube cluster (Bash)
│   └── kurbeScript.ps1       # Starts Minikube cluster (PowerShell)
│
├── ⚙️ Task 1: Basic Deployment
│   └── deployment.yaml        # K8s deployment + service
│
├── 📊 Task 2: Scaling
│   ├── kubctl-0x01           # Scales to 3 replicas (Bash)
│   └── kubctl-0x01.ps1       # Scales to 3 replicas (PowerShell)
│
├── 🌐 Task 3: Ingress
│   ├── ingress.yaml          # External access configuration
│   └── commands.txt          # Setup commands reference
│
├── 🔵🟢 Task 4: Blue-Green Deployment
│   ├── blue_deployment.yaml   # Stable version (v1.0)
│   ├── green_deployment.yaml  # New version (v2.0)
│   ├── kubeservice.yaml       # Switching service
│   ├── kubctl-0x02           # Deployment script (Bash)
│   └── kubctl-0x02.ps1       # Deployment script (PowerShell)
│
└── 🔄 Task 5: Rolling Updates
    ├── kubctl-0x03           # Rolling update script (Bash)
    └── kubctl-0x03.ps1       # Rolling update script (PowerShell)
```

## 🚀 Quick Start

### Step 1: Build the Docker Image

```bash
# Navigate to the messaging_app directory
cd messaging_app

# Build the Docker image
docker build -t messaging-app:latest .

# Tag it for different versions
docker tag messaging-app:latest messaging-app:v1.0
docker tag messaging-app:latest messaging-app:v2.0
```

### Step 2: Start Minikube

```bash
# Linux/macOS
chmod +x kurbeScript
./kurbeScript

# Windows PowerShell
.\kurbeScript.ps1
```

### Step 3: Load Image into Minikube

```bash
# Make the Docker image available to Minikube
minikube image load messaging-app:latest
minikube image load messaging-app:v1.0
minikube image load messaging-app:v2.0

# Verify images are loaded
minikube image ls | grep messaging-app
```

Now you're ready to start the tasks!

## 📋 Tasks Breakdown

### Task 0: Cluster Setup ⚙️

**Goal:** Get a local Kubernetes cluster running

```bash
# Run the setup script
./kurbeScript  # Linux/macOS
.\kurbeScript.ps1  # Windows

# Verify cluster is healthy
kubectl get nodes
kubectl cluster-info
```

**What you learn:**
- Starting a Kubernetes cluster
- Verifying cluster health
- Basic kubectl commands

---

### Task 1: Basic Deployment 📦

**Goal:** Deploy the Django app to Kubernetes

```bash
# Apply the deployment
kubectl apply -f deployment.yaml

# Watch pods start
kubectl get pods -w

# Check deployment status
kubectl get deployment messaging-app-deployment
kubectl get service messaging-app-service

# Test the app (port forward)
kubectl port-forward service/messaging-app-service 8080:80
# Access: http://localhost:8080
```

**What you learn:**
- Creating Kubernetes Deployments
- Defining Services for internal networking
- Resource limits and health checks
- Port forwarding for local testing

**Key Concepts:**
- **Pod:** Smallest deployable unit (runs containers)
- **Deployment:** Manages pod replicas and updates
- **Service:** Provides stable networking for pods

---

### Task 2: Scaling 📊

**Goal:** Scale the app to handle more traffic

```bash
# Run the scaling script
chmod +x kubctl-0x01
./kubctl-0x01  # Linux/macOS
.\kubctl-0x01.ps1  # Windows

# Manual scaling
kubectl scale deployment messaging-app-deployment --replicas=3

# Watch pods scale up
kubectl get pods -l app=messaging-app -w

# Check load distribution
kubectl get pods -o wide
```

**What you learn:**
- Horizontal scaling (adding more pods)
- Load balancing across replicas
- Monitoring resource usage
- High availability concepts

**Key Metrics:**
- Number of replicas
- Pod distribution across nodes
- CPU and memory usage

---

### Task 3: Ingress (External Access) 🌐

**Goal:** Expose the app to the internet

```bash
# Enable Ingress in Minikube
minikube addons enable ingress

# Verify Ingress controller
kubectl get pods -n ingress-nginx

# Apply Ingress configuration
kubectl apply -f ingress.yaml

# Get Minikube IP
minikube ip

# Access the app
curl http://$(minikube ip)/messaging

# Or add to hosts file
echo "$(minikube ip) messaging-app.local" | sudo tee -a /etc/hosts
# Then visit: http://messaging-app.local
```

**What you learn:**
- Ingress controllers (smart routing)
- Path-based routing
- Host-based routing
- External load balancing

**Production Use:**
- Replace Minikube IP with real domain
- Add TLS/SSL certificates
- Configure DNS records

---

### Task 4: Blue-Green Deployment 🔵🟢

**Goal:** Deploy new versions without downtime, with instant rollback

```bash
# Run the blue-green script
chmod +x kubctl-0x02
./kubctl-0x02  # Linux/macOS
.\kubctl-0x02.ps1  # Windows

# The script will:
# 1. Deploy BLUE version (v1.0)
# 2. Deploy GREEN version (v2.0) in parallel
# 3. Test GREEN privately
# 4. Switch traffic to GREEN
# 5. Keep BLUE running for quick rollback

# Manual rollback if needed
kubectl patch service messaging-app-bluegreen-service \
  -p '{"spec":{"selector":{"deployment":"blue"}}}'
```

**What you learn:**
- Zero-downtime deployments
- Instant rollback capability
- Running multiple versions simultaneously
- Traffic switching strategies

**When to use:**
- Major version updates
- High-risk deployments
- Need instant rollback
- A/B testing

**Pros:**
✅ Instant rollback  
✅ Zero downtime  
✅ Test before switching  

**Cons:**
❌ Requires 2x resources  
❌ More complex setup  

---

### Task 5: Rolling Updates 🔄

**Goal:** Update automatically with zero downtime

```bash
# Run the rolling update script
chmod +x kubctl-0x03
./kubctl-0x03  # Linux/macOS
.\kubctl-0x03.ps1  # Windows

# Manual rolling update
kubectl set image deployment/messaging-app-deployment \
  messaging-app=messaging-app:v2.0

# Watch the rollout
kubectl rollout status deployment/messaging-app-deployment

# Check rollout history
kubectl rollout history deployment/messaging-app-deployment

# Rollback if needed
kubectl rollout undo deployment/messaging-app-deployment

# Rollback to specific revision
kubectl rollout undo deployment/messaging-app-deployment --to-revision=2
```

**What you learn:**
- Automated gradual updates
- Zero downtime deployments
- Rollout strategies (maxSurge, maxUnavailable)
- Automatic rollback on failure

**Rolling Update Strategy:**
- `maxSurge: 1` - Create 1 extra pod during update
- `maxUnavailable: 0` - No downtime allowed

**When to use:**
- Regular updates
- Low-risk deployments
- Limited resources
- Gradual rollout preferred

**Pros:**
✅ Automated process  
✅ Resource efficient  
✅ Built-in to Kubernetes  

**Cons:**
❌ Slower than blue-green  
❌ Rollback takes time  

---

## 🎓 Learning Objectives

By completing this tutorial, you'll understand:

### Containerization
- Docker image creation
- Container registries
- Multi-stage builds
- Image optimization

### Kubernetes Concepts
- **Pods:** Smallest deployable units
- **Deployments:** Manage pod replicas
- **Services:** Stable networking
- **Ingress:** External access routing
- **Labels & Selectors:** Resource organization

### Deployment Strategies
| Strategy | Downtime | Rollback Speed | Resource Usage | Use Case |
|----------|----------|----------------|----------------|----------|
| **Basic** | Yes | N/A | Low | Development |
| **Rolling** | No | Slow | Low | Regular updates |
| **Blue-Green** | No | Instant | High | Critical apps |
| **Canary** | No | Medium | Medium | Gradual rollout |

### DevOps Practices
- Infrastructure as Code (IaC)
- GitOps workflows
- Monitoring and observability
- Disaster recovery

### Production Skills
- Resource management (CPU, memory)
- Health checks (liveness, readiness)
- Horizontal pod autoscaling
- Load balancing

---

## 🔧 Troubleshooting

### Common Issues

#### Pods not starting
```bash
# Check pod status
kubectl get pods

# View pod logs
kubectl logs <pod-name>

# Describe pod for events
kubectl describe pod <pod-name>

# Common causes:
# - Image pull errors → Check image name/tag
# - Resource limits → Increase memory/CPU
# - Crash loops → Check application logs
```

#### Service not accessible
```bash
# Check service
kubectl get service messaging-app-service

# Check endpoints
kubectl get endpoints messaging-app-service

# Port forward to test
kubectl port-forward service/messaging-app-service 8080:80

# Common causes:
# - Wrong selector labels
# - Pods not ready
# - Port mismatch
```

#### Ingress not working
```bash
# Check Ingress status
kubectl get ingress

# Describe Ingress
kubectl describe ingress messaging-app-ingress

# Check Ingress controller
kubectl get pods -n ingress-nginx

# View Ingress logs
kubectl logs -n ingress-nginx <ingress-controller-pod>

# Common causes:
# - Ingress addon not enabled
# - Wrong service name
# - Path routing issues
```

#### Minikube issues
```bash
# Restart Minikube
minikube stop
minikube start

# Delete and recreate
minikube delete
minikube start

# Check Minikube status
minikube status

# View Minikube logs
minikube logs
```

### Useful Commands

```bash
# Get all resources
kubectl get all

# Watch resources in real-time
kubectl get pods -w

# Get detailed info
kubectl describe <resource-type> <resource-name>

# View logs
kubectl logs <pod-name>
kubectl logs -f <pod-name>  # Follow logs

# Execute commands in pod
kubectl exec -it <pod-name> -- /bin/bash

# Delete resources
kubectl delete -f <file.yaml>
kubectl delete pod <pod-name>

# Clean up everything
kubectl delete deployment --all
kubectl delete service --all
kubectl delete ingress --all
```

---

## 📚 Additional Resources

### Official Documentation
- [Kubernetes Docs](https://kubernetes.io/docs/)
- [Minikube Docs](https://minikube.sigs.k8s.io/docs/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Django Deployment](https://docs.djangoproject.com/en/stable/howto/deployment/)

### Learning Paths
- [Kubernetes Basics Tutorial](https://kubernetes.io/docs/tutorials/kubernetes-basics/)
- [Kubernetes Deployment Strategies](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Production Best Practices](https://kubernetes.io/docs/setup/best-practices/)

### Community
- [Kubernetes Slack](https://slack.k8s.io/)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/kubernetes)
- [Reddit r/kubernetes](https://reddit.com/r/kubernetes)

---

## 🎯 Next Steps

After completing this tutorial:

1. **Add Monitoring:**
   - Install Prometheus and Grafana
   - Set up custom metrics
   - Create dashboards

2. **Implement CI/CD:**
   - GitHub Actions for automated builds
   - ArgoCD for GitOps
   - Automated testing

3. **Advanced Strategies:**
   - Canary deployments
   - A/B testing
   - Feature flags

4. **Production Hardening:**
   - Network policies
   - Pod security policies
   - Secrets management
   - TLS/SSL certificates

5. **Cloud Migration:**
   - Deploy to GKE, EKS, or AKS
   - Set up managed Kubernetes
   - Configure cloud load balancers

---

## 📝 License

This project is for educational purposes as part of the ALX Backend Python specialization.

---

## 🙏 Acknowledgments

- ALX Africa for the curriculum
- Kubernetes community for excellent documentation
- Django team for the robust framework

---

**Happy Learning! 🚀**

If you encounter any issues or have questions, refer to the troubleshooting section or reach out to the community.

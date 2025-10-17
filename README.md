# 📘 ALX Backend Python - Kubernetes Projects

Welcome to the Kubernetes deployment section of the ALX Backend Python specialization!

## 🎯 What's Inside

This repository contains multiple Django projects demonstrating various backend concepts, with a **special focus on Kubernetes deployment strategies** in the `messaging_app` folder.

## 📁 Repository Structure

```
alx-backend-python/
├── 0x03-Unittests_and_integration_tests/   # Testing best practices
├── Django-Middleware-0x03/                  # Custom middleware
├── Django-signals_orm-0x04/                 # Signals and ORM
└── messaging_app/                           # 🚀 KUBERNETES DEPLOYMENT PROJECT
    ├── Complete Django messaging application
    ├── Docker containerization
    └── Full Kubernetes deployment tutorial
```

## 🚀 Featured Project: Messaging App with Kubernetes

The **messaging_app** folder contains a comprehensive, production-ready Kubernetes deployment tutorial.

### What You'll Learn

✅ **Containerization with Docker**  
✅ **Kubernetes orchestration**  
✅ **Horizontal scaling**  
✅ **Zero-downtime deployments**  
✅ **Blue-Green deployment strategy**  
✅ **Rolling updates**  
✅ **Ingress and load balancing**

### Quick Start

```bash
# Navigate to the messaging app
cd messaging_app

# Read the complete tutorial
cat KUBERNETES_TUTORIAL.md

# Or if you're ready to dive in:

# 1. Build the Docker image
docker build -t messaging-app:latest .
docker tag messaging-app:latest messaging-app:v1.0
docker tag messaging-app:latest messaging-app:v2.0

# 2. Start Minikube cluster
# Linux/macOS:
./kurbeScript
# Windows PowerShell:
.\kurbeScript.ps1

# 3. Load images into Minikube
minikube image load messaging-app:latest
minikube image load messaging-app:v1.0
minikube image load messaging-app:v2.0

# 4. Deploy to Kubernetes
kubectl apply -f deployment.yaml

# 5. Verify deployment
kubectl get pods
kubectl get service messaging-app-service

# 6. Access the app
kubectl port-forward service/messaging-app-service 8080:80
# Visit: http://localhost:8080
```

## 📚 Complete Task List

The messaging_app project includes **6 progressive tasks**:

| Task | Name | Files | What You Learn |
|------|------|-------|----------------|
| **0** | Cluster Setup | `kurbeScript` | Start & verify K8s cluster |
| **1** | Basic Deployment | `deployment.yaml` | Deploy app to Kubernetes |
| **2** | Scaling | `kubctl-0x01` | Scale to 3 replicas |
| **3** | Ingress | `ingress.yaml`, `commands.txt` | External access routing |
| **4** | Blue-Green | `blue_deployment.yaml`, `green_deployment.yaml`, `kubeservice.yaml`, `kubctl-0x02` | Zero-downtime deployment |
| **5** | Rolling Updates | `kubctl-0x03` | Automated gradual updates |

## 🛠️ Prerequisites

Before starting, install:

- **Docker** (v20.10+) - [Install Guide](https://docs.docker.com/get-docker/)
- **Minikube** (v1.25+) - [Install Guide](https://minikube.sigs.k8s.io/docs/start/)
- **kubectl** (v1.23+) - [Install Guide](https://kubernetes.io/docs/tasks/tools/)
- **Python** (v3.8+) - [Install Guide](https://www.python.org/downloads/)

### Quick Install (Windows)

```powershell
# Using Chocolatey
choco install docker-desktop minikube kubernetes-cli python

# Or using Scoop
scoop install docker minikube kubectl python
```

### Quick Install (macOS)

```bash
# Using Homebrew
brew install docker minikube kubectl python
```

### Quick Install (Linux)

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install kubectl /usr/local/bin/kubectl
```

## 📖 Documentation

For the **complete, step-by-step tutorial**, see:

**📄 [messaging_app/KUBERNETES_TUTORIAL.md](./messaging_app/KUBERNETES_TUTORIAL.md)**

This comprehensive guide includes:
- Detailed explanations of each task
- Command references
- Troubleshooting tips
- Best practices
- Production deployment guidance

## 🎓 Learning Path

### Recommended Order

1. **Read** `KUBERNETES_TUTORIAL.md` to understand concepts
2. **Complete Task 0** - Set up your local Kubernetes cluster
3. **Complete Task 1** - Deploy your first app
4. **Complete Task 2** - Learn scaling
5. **Complete Task 3** - Configure external access
6. **Complete Task 4** - Master blue-green deployment
7. **Complete Task 5** - Implement rolling updates

### Time Estimate

- **Quick run-through:** 2-3 hours
- **Deep dive with experimentation:** 1-2 days
- **Production-ready understanding:** 1 week

## 🔍 Other Projects in This Repo

### 0x03-Unittests_and_integration_tests
Learn testing best practices for Python applications.

### Django-Middleware-0x03
Explore custom middleware development in Django.

### Django-signals_orm-0x04
Master Django signals and ORM advanced techniques.

## 🤝 Contributing

This is an educational project. If you find issues or have suggestions:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📝 Notes for Students

- **Scripts:** Both Bash (`.sh`) and PowerShell (`.ps1`) versions provided
- **Platform:** Works on Windows, macOS, and Linux
- **Cloud-Ready:** Concepts transfer directly to AWS EKS, Google GKE, Azure AKS
- **Production:** All examples use production best practices

## 🆘 Need Help?

- **Tutorial:** See `messaging_app/KUBERNETES_TUTORIAL.md`
- **Troubleshooting:** Check the troubleshooting section in the tutorial
- **Commands Reference:** See `messaging_app/commands.txt`
- **Community:** Join Kubernetes Slack or Stack Overflow

## 🎯 After Completing This Tutorial

You'll be able to:

✅ Deploy containerized applications to Kubernetes  
✅ Scale applications horizontally  
✅ Implement zero-downtime deployments  
✅ Choose the right deployment strategy for your use case  
✅ Troubleshoot common Kubernetes issues  
✅ Apply these skills to real-world projects  

## 📚 Additional Resources

- [Kubernetes Official Docs](https://kubernetes.io/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [12-Factor App Methodology](https://12factor.net/)

## 🚀 Ready to Start?

```bash
cd messaging_app
cat KUBERNETES_TUTORIAL.md
```

**Happy Learning! 🎉**

---

**Project maintained by:** FredrickMbithi  
**Course:** ALX Backend Python Specialization  
**Last Updated:** October 2025

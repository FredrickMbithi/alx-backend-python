# 🚀 Kubernetes Quick Reference - Messaging App

## 📋 One-Command Quick Start

```bash
# Complete setup in one go (Linux/macOS)
cd messaging_app && \
docker build -t messaging-app:latest . && \
docker tag messaging-app:latest messaging-app:v1.0 && \
docker tag messaging-app:latest messaging-app:v2.0 && \
./kurbeScript && \
minikube image load messaging-app:latest && \
minikube image load messaging-app:v1.0 && \
minikube image load messaging-app:v2.0 && \
kubectl apply -f deployment.yaml
```

```powershell
# Complete setup in one go (Windows PowerShell)
cd messaging_app
docker build -t messaging-app:latest .
docker tag messaging-app:latest messaging-app:v1.0
docker tag messaging-app:latest messaging-app:v2.0
.\kurbeScript.ps1
minikube image load messaging-app:latest
minikube image load messaging-app:v1.0
minikube image load messaging-app:v2.0
kubectl apply -f deployment.yaml
```

## 🎯 Task Commands

### Task 0: Cluster Setup
```bash
# Linux/macOS
./kurbeScript

# Windows
.\kurbeScript.ps1

# Verify
kubectl get nodes
kubectl cluster-info
```

### Task 1: Basic Deployment
```bash
# Deploy
kubectl apply -f deployment.yaml

# Check status
kubectl get pods
kubectl get deployment
kubectl get service

# Access app
kubectl port-forward service/messaging-app-service 8080:80
# Visit: http://localhost:8080
```

### Task 2: Scaling
```bash
# Run script
./kubctl-0x01          # Linux/macOS
.\kubctl-0x01.ps1      # Windows

# Or manually
kubectl scale deployment messaging-app-deployment --replicas=3

# Verify
kubectl get pods -l app=messaging-app
```

### Task 3: Ingress
```bash
# Enable Ingress
minikube addons enable ingress

# Deploy Ingress
kubectl apply -f ingress.yaml

# Get Minikube IP
minikube ip

# Access
curl http://$(minikube ip)/messaging
```

### Task 4: Blue-Green
```bash
# Run script
./kubctl-0x02          # Linux/macOS
.\kubctl-0x02.ps1      # Windows

# Or manually:
kubectl apply -f blue_deployment.yaml
kubectl apply -f green_deployment.yaml
kubectl apply -f kubeservice.yaml

# Switch to GREEN
kubectl patch service messaging-app-bluegreen-service \
  -p '{"spec":{"selector":{"deployment":"green"}}}'

# Rollback to BLUE
kubectl patch service messaging-app-bluegreen-service \
  -p '{"spec":{"selector":{"deployment":"blue"}}}'
```

### Task 5: Rolling Update
```bash
# Run script
./kubctl-0x03          # Linux/macOS
.\kubctl-0x03.ps1      # Windows

# Or manually
kubectl set image deployment/messaging-app-deployment \
  messaging-app=messaging-app:v2.0

# Watch rollout
kubectl rollout status deployment/messaging-app-deployment

# Rollback
kubectl rollout undo deployment/messaging-app-deployment
```

## 🔍 Essential kubectl Commands

### Viewing Resources
```bash
kubectl get all                              # All resources
kubectl get pods                             # All pods
kubectl get pods -o wide                     # Pods with more details
kubectl get pods -w                          # Watch pods (live updates)
kubectl get deployment                       # Deployments
kubectl get service                          # Services
kubectl get ingress                          # Ingress rules
```

### Describing Resources
```bash
kubectl describe pod <pod-name>              # Pod details
kubectl describe deployment <deployment>     # Deployment details
kubectl describe service <service>           # Service details
kubectl describe ingress <ingress>           # Ingress details
```

### Logs and Debugging
```bash
kubectl logs <pod-name>                      # View logs
kubectl logs -f <pod-name>                   # Follow logs (live)
kubectl logs <pod-name> --previous          # Previous container logs
kubectl exec -it <pod-name> -- /bin/bash    # Shell into pod
kubectl top pods                             # Resource usage
kubectl top nodes                            # Node resource usage
```

### Editing Resources
```bash
kubectl edit deployment <name>               # Edit deployment
kubectl edit service <name>                  # Edit service
kubectl scale deployment <name> --replicas=5 # Scale deployment
kubectl delete pod <pod-name>                # Delete pod
kubectl delete -f <file.yaml>                # Delete from file
```

### Rollouts
```bash
kubectl rollout status deployment/<name>     # Rollout status
kubectl rollout history deployment/<name>    # Rollout history
kubectl rollout undo deployment/<name>       # Rollback last
kubectl rollout undo deployment/<name> --to-revision=2  # Rollback to specific
kubectl rollout pause deployment/<name>      # Pause rollout
kubectl rollout resume deployment/<name>     # Resume rollout
```

### Port Forwarding
```bash
kubectl port-forward pod/<pod> 8080:8000    # Forward pod port
kubectl port-forward service/<svc> 8080:80  # Forward service port
kubectl port-forward deployment/<dep> 8080:8000  # Forward deployment port
```

## 🛠️ Minikube Commands

```bash
minikube start                               # Start cluster
minikube stop                                # Stop cluster
minikube delete                              # Delete cluster
minikube status                              # Cluster status
minikube ip                                  # Get cluster IP
minikube dashboard                           # Open web dashboard
minikube ssh                                 # SSH into Minikube VM
minikube addons list                         # List addons
minikube addons enable ingress               # Enable Ingress
minikube image load <image>                  # Load Docker image
minikube image ls                            # List loaded images
minikube service <service-name>              # Open service in browser
minikube tunnel                              # Route LoadBalancer services
```

## 🐳 Docker Commands

```bash
docker build -t messaging-app:latest .       # Build image
docker images                                # List images
docker tag <source> <target>                 # Tag image
docker rmi <image>                           # Remove image
docker ps                                    # Running containers
docker ps -a                                 # All containers
docker logs <container>                      # Container logs
docker exec -it <container> /bin/bash        # Shell into container
```

## 🚨 Troubleshooting Quick Fixes

### Pods Not Starting
```bash
# Check pod status
kubectl get pods

# View pod details
kubectl describe pod <pod-name>

# View logs
kubectl logs <pod-name>

# Delete and recreate
kubectl delete pod <pod-name>
```

### Image Pull Errors
```bash
# Verify image exists in Minikube
minikube image ls | grep messaging-app

# Reload image
minikube image load messaging-app:latest

# Check imagePullPolicy in YAML (should be "Never" for local)
```

### Service Not Accessible
```bash
# Check service endpoints
kubectl get endpoints <service-name>

# Check if pods are ready
kubectl get pods

# Test with port-forward
kubectl port-forward service/<service> 8080:80
```

### Ingress Not Working
```bash
# Check if Ingress addon is enabled
minikube addons list | grep ingress

# Enable if needed
minikube addons enable ingress

# Check Ingress controller pods
kubectl get pods -n ingress-nginx

# View Ingress details
kubectl describe ingress <ingress-name>
```

### Clean Slate
```bash
# Delete all resources
kubectl delete deployment --all
kubectl delete service --all
kubectl delete ingress --all

# Or restart Minikube
minikube delete
minikube start
```

## 📊 Resource Management

### Set Resource Limits
```yaml
resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "256Mi"
    cpu: "500m"
```

### Autoscaling
```bash
# Enable autoscaling
kubectl autoscale deployment <name> --min=2 --max=10 --cpu-percent=80

# View HPA
kubectl get hpa

# Delete HPA
kubectl delete hpa <name>
```

## 🔐 Security Best Practices

```bash
# Create secret
kubectl create secret generic app-secret --from-literal=key=value

# Use secret in deployment
env:
  - name: SECRET_KEY
    valueFrom:
      secretKeyRef:
        name: app-secret
        key: key

# View secrets
kubectl get secrets
```

## 📈 Monitoring

```bash
# Install metrics-server
minikube addons enable metrics-server

# View metrics
kubectl top nodes
kubectl top pods

# Dashboard
minikube dashboard
```

## 🎯 Pro Tips

1. **Use Labels:** Organize resources with labels
   ```bash
   kubectl get pods -l app=messaging-app
   kubectl get all -l version=blue
   ```

2. **Use Namespaces:** Separate environments
   ```bash
   kubectl create namespace staging
   kubectl apply -f deployment.yaml -n staging
   ```

3. **Dry Run:** Test YAML before applying
   ```bash
   kubectl apply -f deployment.yaml --dry-run=client
   ```

4. **Watch Resources:** Monitor in real-time
   ```bash
   kubectl get pods -w
   watch kubectl get pods
   ```

5. **Save Resources:** Export for backup
   ```bash
   kubectl get deployment messaging-app-deployment -o yaml > backup.yaml
   ```

## ⌨️ Bash Aliases (Optional)

Add to `~/.bashrc` or `~/.bash_profile`:

```bash
alias k='kubectl'
alias kgp='kubectl get pods'
alias kgs='kubectl get services'
alias kgd='kubectl get deployments'
alias kl='kubectl logs'
alias kex='kubectl exec -it'
alias kdel='kubectl delete'
alias kdes='kubectl describe'
alias m='minikube'
```

Then use: `k get pods` instead of `kubectl get pods`

## 🎓 Next Level

After mastering these basics:

1. **Helm:** Package manager for Kubernetes
2. **Prometheus & Grafana:** Monitoring and alerting
3. **ArgoCD:** GitOps continuous delivery
4. **Istio:** Service mesh for microservices
5. **Cert-Manager:** Automated TLS certificates

---

**Save this file for quick reference!** 📌

Print it or keep it open while working through the tasks.

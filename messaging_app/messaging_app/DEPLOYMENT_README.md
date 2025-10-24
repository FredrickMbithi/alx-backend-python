# 🚀 Django Messaging App - Kubernetes Deployment

A production-ready Django messaging application deployed on Kubernetes with comprehensive automation scripts.

## 📋 Quick Start

### Prerequisites

- **Docker** (20.10+)
- **Minikube** (1.25+)
- **kubectl** (1.23+)
- **Python** (3.8+)

### One-Command Deployment

**Windows PowerShell:**

```powershell
.\deploy.ps1
```

**Linux/macOS/Git Bash:**

```bash
chmod +x deploy.sh
./deploy.sh
```

### Manual Deployment Steps

1. **Build Docker Image:**

   ```bash
   docker build -t messaging-app:latest .
   docker tag messaging-app:latest messaging-app:v1.0
   ```

2. **Start Minikube:**

   ```bash
   minikube start
   ```

3. **Load Image into Minikube:**

   ```bash
   minikube image load messaging-app:latest
   ```

4. **Deploy to Kubernetes:**

   ```bash
   kubectl apply -f deployment.yaml
   ```

5. **Wait for Deployment:**

   ```bash
   kubectl wait --for=condition=available deployment/django-messaging-app --timeout=300s
   ```

6. **Access the Application:**
   ```bash
   kubectl port-forward service/django-messaging-service 8080:80
   ```
   Then visit: http://localhost:8080

## 📁 Deployment Files

| File                  | Description                                 |
| --------------------- | ------------------------------------------- |
| `deployment.yaml`     | Main Kubernetes deployment + service        |
| `deploy.sh`           | Complete deployment automation (Bash)       |
| `deploy.ps1`          | Complete deployment automation (PowerShell) |
| `test-deployment.sh`  | Deployment verification (Bash)              |
| `test-deployment.ps1` | Deployment verification (PowerShell)        |

## 🔍 Verification

Run the test script to verify your deployment:

**Windows:**

```powershell
.\test-deployment.ps1
```

**Linux/macOS:**

```bash
chmod +x test-deployment.sh
./test-deployment.sh
```

### Expected Output

- ✅ Deployment is available and ready
- ✅ Pod(s) are running
- ✅ Service exists with endpoints
- ✅ Application is responding

## 📊 Monitoring Commands

```bash
# View all resources
kubectl get all -l app=django-messaging-app

# Check pod logs
kubectl logs -l app=django-messaging-app

# Describe deployment
kubectl describe deployment django-messaging-app

# Check service endpoints
kubectl get endpoints django-messaging-service

# Watch pods in real-time
kubectl get pods -l app=django-messaging-app -w
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. Image Pull Error

```bash
# Verify image is loaded in Minikube
minikube image ls | grep messaging-app

# Reload image if needed
minikube image load messaging-app:latest
```

#### 2. Pod Crash Loop

```bash
# Check pod logs
kubectl logs -l app=django-messaging-app

# Check pod events
kubectl describe pod -l app=django-messaging-app
```

#### 3. Service Not Accessible

```bash
# Check service
kubectl get service django-messaging-service

# Check endpoints
kubectl get endpoints django-messaging-service

# Test with port-forward
kubectl port-forward service/django-messaging-service 8080:80
```

### Debug Commands

```bash
# Get detailed pod information
kubectl describe pod -l app=django-messaging-app

# Check deployment events
kubectl describe deployment django-messaging-app

# View recent events
kubectl get events --sort-by=.metadata.creationTimestamp

# Access pod shell
kubectl exec -it <pod-name> -- /bin/bash
```

## ⚙️ Configuration

### Environment Variables

The deployment includes these environment variables:

- `DEBUG=True` - Django debug mode
- `ALLOWED_HOSTS=*` - Allow all hosts
- `DB_ENGINE=django.db.backends.sqlite3` - Database engine

### Resource Limits

- **Memory:** 128Mi (request), 256Mi (limit)
- **CPU:** 100m (request), 500m (limit)

### Health Checks

- **Liveness Probe:** HTTP GET / (30s delay, 10s interval)
- **Readiness Probe:** HTTP GET / (5s delay, 5s interval)

## 🔧 Customization

### Modify Resources

Edit `deployment.yaml` to change resource limits:

```yaml
resources:
  requests:
    memory: "256Mi" # Increase memory request
    cpu: "200m" # Increase CPU request
  limits:
    memory: "512Mi" # Increase memory limit
    cpu: "1000m" # Increase CPU limit
```

### Scale Replicas

```bash
# Scale to 3 replicas
kubectl scale deployment django-messaging-app --replicas=3

# Or edit deployment.yaml and change:
# spec:
#   replicas: 3
```

### Add Environment Variables

Add to `deployment.yaml`:

```yaml
env:
  - name: MY_CUSTOM_VAR
    value: "my_value"
  - name: SECRET_KEY
    valueFrom:
      secretKeyRef:
        name: django-secrets
        key: secret-key
```

## 🚀 Advanced Deployment

### Using Secrets

```bash
# Create secret
kubectl create secret generic django-secrets \
  --from-literal=secret-key=your-secret-key

# Reference in deployment.yaml
env:
  - name: SECRET_KEY
    valueFrom:
      secretKeyRef:
        name: django-secrets
        key: secret-key
```

### Persistent Storage

Add to `deployment.yaml`:

```yaml
volumeMounts:
  - name: data
    mountPath: /app/data
volumes:
  - name: data
    persistentVolumeClaim:
      claimName: django-data
```

### Ingress for External Access

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: django-messaging-ingress
spec:
  rules:
    - host: messaging.local
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: django-messaging-service
                port:
                  number: 80
```

## 📈 Production Considerations

### Security

- Remove `DEBUG=True` in production
- Use proper secrets management
- Implement network policies
- Use non-root containers

### Performance

- Add horizontal pod autoscaling
- Configure resource requests/limits properly
- Use production database (PostgreSQL)
- Add Redis for caching

### Monitoring

- Add Prometheus metrics
- Configure log aggregation
- Set up health check endpoints
- Monitor resource usage

## 🎯 Next Steps

1. **Scale the Application:**

   ```bash
   kubectl scale deployment django-messaging-app --replicas=3
   ```

2. **Add Ingress for External Access:**

   ```bash
   minikube addons enable ingress
   kubectl apply -f ingress.yaml
   ```

3. **Implement Blue-Green Deployment:**

   ```bash
   .\kubctl-0x02.ps1  # Windows
   ./kubctl-0x02      # Linux/macOS
   ```

4. **Set up Rolling Updates:**
   ```bash
   .\kubctl-0x03.ps1  # Windows
   ./kubctl-0x03      # Linux/macOS
   ```

## 📚 Documentation

- [Kubernetes Tutorial](./KUBERNETES_TUTORIAL.md) - Complete learning guide
- [Quick Reference](./QUICK_REFERENCE.md) - Command cheat sheet
- [Start Here](./START_HERE.txt) - Project overview

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review the logs: `kubectl logs -l app=django-messaging-app`
3. Verify prerequisites are installed
4. Ensure Minikube is running: `minikube status`

---

**Happy Deploying! 🎉**

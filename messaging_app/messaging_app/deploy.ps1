# deploy.ps1 - Complete deployment script for Django Messaging App on Kubernetes (PowerShell)

Write-Host "🚀 Deploying Django Messaging App to Kubernetes" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Verify prerequisites
Write-Host "📋 Step 1: Checking prerequisites..." -ForegroundColor Yellow

# Check if Docker is running
try {
    $dockerInfo = docker info 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Docker not running"
    }
}
catch {
    Write-Host "❌ Docker is not running. Please start Docker and try again." -ForegroundColor Red
    exit 1
}

# Check if Minikube is running
try {
    $minikubeStatus = minikube status 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️  Minikube is not running. Starting Minikube..." -ForegroundColor Yellow
        minikube start
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Failed to start Minikube. Please check your installation." -ForegroundColor Red
            exit 1
        }
    }
}
catch {
    Write-Host "❌ Minikube is not available. Please install Minikube and try again." -ForegroundColor Red
    exit 1
}

# Check if kubectl is available
try {
    $kubectlVersion = kubectl version --client 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "kubectl not found"
    }
}
catch {
    Write-Host "❌ kubectl is not installed. Please install kubectl and try again." -ForegroundColor Red
    exit 1
}

Write-Host "✅ All prerequisites are met!" -ForegroundColor Green
Write-Host ""

# Step 2: Build the Docker image
Write-Host "🐳 Step 2: Building Docker image..." -ForegroundColor Yellow
docker build -t messaging-app:latest .
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to build Docker image." -ForegroundColor Red
    exit 1
}

# Tag the image for different versions
docker tag messaging-app:latest messaging-app:v1.0
docker tag messaging-app:latest messaging-app:v2.0

Write-Host "✅ Docker image built successfully!" -ForegroundColor Green
Write-Host ""

# Step 3: Load image into Minikube
Write-Host "📦 Step 3: Loading image into Minikube..." -ForegroundColor Yellow
minikube image load messaging-app:latest
minikube image load messaging-app:v1.0
minikube image load messaging-app:v2.0

Write-Host "✅ Images loaded into Minikube!" -ForegroundColor Green
Write-Host ""

# Step 4: Apply Kubernetes configurations
Write-Host "⚙️  Step 4: Deploying to Kubernetes..." -ForegroundColor Yellow

# Apply the deployment
kubectl apply -f deployment.yaml
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to apply deployment.yaml" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Deployment applied successfully!" -ForegroundColor Green
Write-Host ""

# Step 5: Wait for deployment to be ready
Write-Host "⏳ Step 5: Waiting for deployment to be ready..." -ForegroundColor Yellow
kubectl wait --for=condition=available deployment/django-messaging-app --timeout=300s

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Deployment did not become ready within 5 minutes." -ForegroundColor Red
    Write-Host "Checking pod status:" -ForegroundColor Yellow
    kubectl get pods -l app=django-messaging-app
    Write-Host ""
    Write-Host "Pod logs:" -ForegroundColor Yellow
    kubectl logs -l app=django-messaging-app
    exit 1
}

Write-Host "✅ Deployment is ready!" -ForegroundColor Green
Write-Host ""

# Step 6: Display deployment status
Write-Host "📊 Step 6: Deployment Status" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan
Write-Host ""

Write-Host "🔍 Pods:" -ForegroundColor Yellow
kubectl get pods -l app=django-messaging-app -o wide
Write-Host ""

Write-Host "🔍 Services:" -ForegroundColor Yellow
kubectl get services django-messaging-service
Write-Host ""

Write-Host "🔍 Deployment:" -ForegroundColor Yellow
kubectl get deployment django-messaging-app
Write-Host ""

# Step 7: Provide access instructions
Write-Host "🌐 Step 7: Access Your Application" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Your Django Messaging App is now running on Kubernetes!" -ForegroundColor Green
Write-Host ""

Write-Host "To access the application, run:" -ForegroundColor Yellow
Write-Host "  kubectl port-forward service/django-messaging-service 8080:80" -ForegroundColor White
Write-Host ""
Write-Host "Then open your browser and visit:" -ForegroundColor Yellow
Write-Host "  http://localhost:8080" -ForegroundColor White
Write-Host ""

Write-Host "Other useful commands:" -ForegroundColor Yellow
Write-Host "  kubectl logs -l app=django-messaging-app           # View application logs" -ForegroundColor DarkGray
Write-Host "  kubectl describe pod -l app=django-messaging-app   # Get detailed pod info" -ForegroundColor DarkGray
Write-Host "  kubectl get all -l app=django-messaging-app        # View all related resources" -ForegroundColor DarkGray
Write-Host ""

Write-Host "🎉 Deployment completed successfully!" -ForegroundColor Green
Write-Host ""

# Optional: Start port forwarding automatically
$response = Read-Host "Would you like to start port-forwarding now? (y/n)"
if ($response -eq 'y' -or $response -eq 'Y') {
    Write-Host "🌐 Starting port-forward on http://localhost:8080" -ForegroundColor Cyan
    Write-Host "Press Ctrl+C to stop..." -ForegroundColor Yellow
    kubectl port-forward service/django-messaging-service 8080:80
}
#!/bin/bash

# deploy.sh - Complete deployment script for Django Messaging App on Kubernetes

echo "🚀 Deploying Django Messaging App to Kubernetes"
echo "================================================="
echo ""

# Step 1: Verify prerequisites
echo "📋 Step 1: Checking prerequisites..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if Minikube is running
if ! minikube status > /dev/null 2>&1; then
    echo "⚠️  Minikube is not running. Starting Minikube..."
    minikube start
    if [ $? -ne 0 ]; then
        echo "❌ Failed to start Minikube. Please check your installation."
        exit 1
    fi
fi

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed. Please install kubectl and try again."
    exit 1
fi

echo "✅ All prerequisites are met!"
echo ""

# Step 2: Build the Docker image
echo "🐳 Step 2: Building Docker image..."
docker build -t messaging-app:latest .
if [ $? -ne 0 ]; then
    echo "❌ Failed to build Docker image."
    exit 1
fi

# Tag the image for different versions
docker tag messaging-app:latest messaging-app:v1.0
docker tag messaging-app:latest messaging-app:v2.0

echo "✅ Docker image built successfully!"
echo ""

# Step 3: Load image into Minikube
echo "📦 Step 3: Loading image into Minikube..."
minikube image load messaging-app:latest
minikube image load messaging-app:v1.0
minikube image load messaging-app:v2.0

echo "✅ Images loaded into Minikube!"
echo ""

# Step 4: Apply Kubernetes configurations
echo "⚙️  Step 4: Deploying to Kubernetes..."

# Apply the deployment
kubectl apply -f deployment.yaml
if [ $? -ne 0 ]; then
    echo "❌ Failed to apply deployment.yaml"
    exit 1
fi

echo "✅ Deployment applied successfully!"
echo ""

# Step 5: Wait for deployment to be ready
echo "⏳ Step 5: Waiting for deployment to be ready..."
kubectl wait --for=condition=available deployment/django-messaging-app --timeout=300s

if [ $? -ne 0 ]; then
    echo "❌ Deployment did not become ready within 5 minutes."
    echo "Checking pod status:"
    kubectl get pods -l app=django-messaging-app
    echo ""
    echo "Pod logs:"
    kubectl logs -l app=django-messaging-app
    exit 1
fi

echo "✅ Deployment is ready!"
echo ""

# Step 6: Display deployment status
echo "📊 Step 6: Deployment Status"
echo "============================="
echo ""

echo "🔍 Pods:"
kubectl get pods -l app=django-messaging-app -o wide
echo ""

echo "🔍 Services:"
kubectl get services django-messaging-service
echo ""

echo "🔍 Deployment:"
kubectl get deployment django-messaging-app
echo ""

# Step 7: Provide access instructions
echo "🌐 Step 7: Access Your Application"
echo "=================================="
echo ""

echo "Your Django Messaging App is now running on Kubernetes!"
echo ""

echo "To access the application, run:"
echo "  kubectl port-forward service/django-messaging-service 8080:80"
echo ""
echo "Then open your browser and visit:"
echo "  http://localhost:8080"
echo ""

echo "Other useful commands:"
echo "  kubectl logs -l app=django-messaging-app           # View application logs"
echo "  kubectl describe pod -l app=django-messaging-app   # Get detailed pod info"
echo "  kubectl get all -l app=django-messaging-app        # View all related resources"
echo ""

echo "🎉 Deployment completed successfully!"
echo ""

# Optional: Start port forwarding automatically
read -p "Would you like to start port-forwarding now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🌐 Starting port-forward on http://localhost:8080"
    echo "Press Ctrl+C to stop..."
    kubectl port-forward service/django-messaging-service 8080:80
fi
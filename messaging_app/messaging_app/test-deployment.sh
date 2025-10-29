#!/bin/bash

# test-deployment.sh - Test script to verify the Django Messaging App deployment

echo "🧪 Testing Django Messaging App Deployment"
echo "==========================================="
echo ""

# Test 1: Check if deployment exists and is ready
echo "📋 Test 1: Checking deployment status..."
DEPLOYMENT_STATUS=$(kubectl get deployment django-messaging-app -o jsonpath='{.status.conditions[?(@.type=="Available")].status}' 2>/dev/null)

if [ "$DEPLOYMENT_STATUS" = "True" ]; then
    echo "✅ Deployment is available and ready"
else
    echo "❌ Deployment is not ready"
    kubectl get deployment django-messaging-app
    exit 1
fi

# Test 2: Check if pods are running
echo ""
echo "📋 Test 2: Checking pod status..."
POD_COUNT=$(kubectl get pods -l app=django-messaging-app --field-selector=status.phase=Running --no-headers | wc -l)

if [ "$POD_COUNT" -gt 0 ]; then
    echo "✅ $POD_COUNT pod(s) are running"
    kubectl get pods -l app=django-messaging-app
else
    echo "❌ No pods are running"
    kubectl get pods -l app=django-messaging-app
    echo ""
    echo "Pod logs:"
    kubectl logs -l app=django-messaging-app
    exit 1
fi

# Test 3: Check if service exists and has endpoints
echo ""
echo "📋 Test 3: Checking service status..."
SERVICE_EXISTS=$(kubectl get service django-messaging-service --no-headers 2>/dev/null | wc -l)

if [ "$SERVICE_EXISTS" -gt 0 ]; then
    echo "✅ Service exists"
    kubectl get service django-messaging-service
    
    # Check endpoints
    ENDPOINTS=$(kubectl get endpoints django-messaging-service -o jsonpath='{.subsets[0].addresses[0].ip}' 2>/dev/null)
    if [ -n "$ENDPOINTS" ]; then
        echo "✅ Service has endpoints: $ENDPOINTS"
    else
        echo "⚠️  Service has no endpoints"
    fi
else
    echo "❌ Service does not exist"
    exit 1
fi

# Test 4: Test application connectivity (port-forward test)
echo ""
echo "📋 Test 4: Testing application connectivity..."
echo "Starting port-forward test..."

# Start port-forward in background
kubectl port-forward service/django-messaging-service 8888:80 &
PORT_FORWARD_PID=$!

# Wait a moment for port-forward to establish
sleep 5

# Test HTTP connection
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8888 2>/dev/null || echo "000")

# Clean up port-forward
kill $PORT_FORWARD_PID 2>/dev/null

if [ "$HTTP_STATUS" = "200" ] || [ "$HTTP_STATUS" = "301" ] || [ "$HTTP_STATUS" = "302" ]; then
    echo "✅ Application is responding (HTTP $HTTP_STATUS)"
else
    echo "⚠️  Application may not be responding properly (HTTP $HTTP_STATUS)"
    echo "This could be normal if the Django app needs specific configuration"
fi

echo ""
echo "📊 Final Status Summary"
echo "======================"
echo ""

# Summary of all resources
echo "🔍 All resources with label app=django-messaging-app:"
kubectl get all -l app=django-messaging-app

echo ""
echo "🎯 Quick Access Commands:"
echo "  kubectl port-forward service/django-messaging-service 8080:80"
echo "  kubectl logs -l app=django-messaging-app"
echo "  kubectl describe deployment django-messaging-app"
echo ""

echo "🎉 Deployment test completed!"
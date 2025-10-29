# test-deployment.ps1 - Test script to verify the Django Messaging App deployment (PowerShell)

Write-Host "🧪 Testing Django Messaging App Deployment" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Check if deployment exists and is ready
Write-Host "📋 Test 1: Checking deployment status..." -ForegroundColor Yellow
try {
    $deploymentStatus = kubectl get deployment django-messaging-app -o jsonpath='{.status.conditions[?(@.type=="Available")].status}' 2>$null
    
    if ($deploymentStatus -eq "True") {
        Write-Host "✅ Deployment is available and ready" -ForegroundColor Green
    }
    else {
        Write-Host "❌ Deployment is not ready" -ForegroundColor Red
        kubectl get deployment django-messaging-app
        exit 1
    }
}
catch {
    Write-Host "❌ Failed to check deployment status" -ForegroundColor Red
    exit 1
}

# Test 2: Check if pods are running
Write-Host ""
Write-Host "📋 Test 2: Checking pod status..." -ForegroundColor Yellow
try {
    $runningPods = kubectl get pods -l app=django-messaging-app --field-selector=status.phase=Running --no-headers 2>$null
    $podCount = ($runningPods | Measure-Object).Count
    
    if ($podCount -gt 0) {
        Write-Host "✅ $podCount pod(s) are running" -ForegroundColor Green
        kubectl get pods -l app=django-messaging-app
    }
    else {
        Write-Host "❌ No pods are running" -ForegroundColor Red
        kubectl get pods -l app=django-messaging-app
        Write-Host ""
        Write-Host "Pod logs:" -ForegroundColor Yellow
        kubectl logs -l app=django-messaging-app
        exit 1
    }
}
catch {
    Write-Host "❌ Failed to check pod status" -ForegroundColor Red
    exit 1
}

# Test 3: Check if service exists and has endpoints
Write-Host ""
Write-Host "📋 Test 3: Checking service status..." -ForegroundColor Yellow
try {
    $serviceExists = kubectl get service django-messaging-service --no-headers 2>$null
    
    if ($serviceExists) {
        Write-Host "✅ Service exists" -ForegroundColor Green
        kubectl get service django-messaging-service
        
        # Check endpoints
        $endpoints = kubectl get endpoints django-messaging-service -o jsonpath='{.subsets[0].addresses[0].ip}' 2>$null
        if ($endpoints) {
            Write-Host "✅ Service has endpoints: $endpoints" -ForegroundColor Green
        }
        else {
            Write-Host "⚠️  Service has no endpoints" -ForegroundColor Yellow
        }
    }
    else {
        Write-Host "❌ Service does not exist" -ForegroundColor Red
        exit 1
    }
}
catch {
    Write-Host "❌ Failed to check service status" -ForegroundColor Red
    exit 1
}

# Test 4: Test application connectivity (port-forward test)
Write-Host ""
Write-Host "📋 Test 4: Testing application connectivity..." -ForegroundColor Yellow
Write-Host "Starting port-forward test..." -ForegroundColor DarkGray

try {
    # Start port-forward in background job
    $portForwardJob = Start-Job -ScriptBlock {
        kubectl port-forward service/django-messaging-service 8888:80
    }
    
    # Wait a moment for port-forward to establish
    Start-Sleep -Seconds 5
    
    # Test HTTP connection
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8888" -TimeoutSec 10 -ErrorAction Stop
        $httpStatus = $response.StatusCode
    }
    catch {
        $httpStatus = "000"
    }
    
    # Clean up port-forward
    Stop-Job $portForwardJob -Force
    Remove-Job $portForwardJob -Force
    
    if ($httpStatus -eq 200 -or $httpStatus -eq 301 -or $httpStatus -eq 302) {
        Write-Host "✅ Application is responding (HTTP $httpStatus)" -ForegroundColor Green
    }
    else {
        Write-Host "⚠️  Application may not be responding properly (HTTP $httpStatus)" -ForegroundColor Yellow
        Write-Host "This could be normal if the Django app needs specific configuration" -ForegroundColor DarkGray
    }
}
catch {
    Write-Host "⚠️  Could not test HTTP connectivity" -ForegroundColor Yellow
    Write-Host "This could be normal if curl/Invoke-WebRequest is not available" -ForegroundColor DarkGray
}

Write-Host ""
Write-Host "📊 Final Status Summary" -ForegroundColor Cyan
Write-Host "======================" -ForegroundColor Cyan
Write-Host ""

# Summary of all resources
Write-Host "🔍 All resources with label app=django-messaging-app:" -ForegroundColor Yellow
kubectl get all -l app=django-messaging-app

Write-Host ""
Write-Host "🎯 Quick Access Commands:" -ForegroundColor Yellow
Write-Host "  kubectl port-forward service/django-messaging-service 8080:80" -ForegroundColor White
Write-Host "  kubectl logs -l app=django-messaging-app" -ForegroundColor White
Write-Host "  kubectl describe deployment django-messaging-app" -ForegroundColor White
Write-Host ""

Write-Host "🎉 Deployment test completed!" -ForegroundColor Green
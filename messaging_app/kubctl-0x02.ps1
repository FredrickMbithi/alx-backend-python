# kubctl-0x02.ps1 - Task 4: Blue-Green Deployment (PowerShell)
# This script demonstrates blue-green deployment strategy

Write-Host "🔵🟢 Task 4: Blue-Green Deployment" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Deploy Blue (v1.0) - Current stable version
Write-Host "🔵 Step 1: Deploying BLUE version (v1.0)..." -ForegroundColor Blue
kubectl apply -f blue_deployment.yaml

Write-Host ""
Write-Host "⏳ Waiting for blue deployment to be ready..." -ForegroundColor Yellow
kubectl wait --for=condition=available deployment/messaging-app-blue --timeout=60s

Write-Host ""
Write-Host "✅ Blue deployment status:" -ForegroundColor Green
kubectl get deployment messaging-app-blue
kubectl get pods -l version=blue

Write-Host ""
Write-Host "🔵 Step 2: Creating service pointing to BLUE..." -ForegroundColor Blue
kubectl apply -f kubeservice.yaml

Write-Host ""
Write-Host "⏳ Waiting for service to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host ""
Write-Host "🧪 Testing BLUE version..." -ForegroundColor Yellow
kubectl get service messaging-app-bluegreen-service
Write-Host "Current traffic is going to BLUE deployment (v1.0)" -ForegroundColor Cyan

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
Write-Host ""

# Step 2: Deploy Green (v2.0) - New version
Write-Host "🟢 Step 3: Deploying GREEN version (v2.0) in parallel..." -ForegroundColor Green
kubectl apply -f green_deployment.yaml

Write-Host ""
Write-Host "⏳ Waiting for green deployment to be ready..." -ForegroundColor Yellow
kubectl wait --for=condition=available deployment/messaging-app-green --timeout=60s

Write-Host ""
Write-Host "✅ Green deployment status:" -ForegroundColor Green
kubectl get deployment messaging-app-green
kubectl get pods -l version=green

Write-Host ""
Write-Host "📊 Both versions are now running:" -ForegroundColor Cyan
kubectl get deployments -l app=messaging-app
kubectl get pods -l app=messaging-app -o wide

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
Write-Host ""

# Step 3: Test Green version privately
Write-Host "🧪 Step 4: Testing GREEN version (v2.0) privately..." -ForegroundColor Yellow
Write-Host "You can test green via its dedicated service:" -ForegroundColor Cyan
kubectl get service messaging-app-green-service
Write-Host ""
Write-Host "Run this to test GREEN: kubectl port-forward service/messaging-app-green-service 8001:80" -ForegroundColor DarkYellow
Write-Host "Then access: http://localhost:8001" -ForegroundColor DarkYellow

Write-Host ""
Read-Host "Press Enter when ready to switch traffic to GREEN"

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
Write-Host ""

# Step 4: Switch traffic to Green
Write-Host "🔄 Step 5: Switching traffic from BLUE to GREEN..." -ForegroundColor Magenta
kubectl patch service messaging-app-bluegreen-service -p '{\"spec\":{\"selector\":{\"deployment\":\"green\"}}}'

Write-Host ""
Write-Host "✅ Traffic switched! Main service now points to GREEN (v2.0)" -ForegroundColor Green
kubectl get service messaging-app-bluegreen-service -o wide

Write-Host ""
Write-Host "🧪 Verify the switch:" -ForegroundColor Yellow
kubectl describe service messaging-app-bluegreen-service | Select-String -Pattern "Selector" -Context 0, 5

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
Write-Host ""

# Monitor both deployments
Write-Host "📊 Final status - Both versions still running:" -ForegroundColor Cyan
kubectl get deployments -l app=messaging-app
kubectl get pods -l app=messaging-app

Write-Host ""
Write-Host "🎉 Blue-Green deployment complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Summary:" -ForegroundColor Cyan
Write-Host "  🔵 BLUE (v1.0) is still running but not receiving traffic" -ForegroundColor Blue
Write-Host "  🟢 GREEN (v2.0) is now live and handling all requests" -ForegroundColor Green
Write-Host ""
Write-Host "To rollback to BLUE if issues occur:" -ForegroundColor Yellow
Write-Host '  kubectl patch service messaging-app-bluegreen-service -p ''{"spec":{"selector":{"deployment":"blue"}}}''' -ForegroundColor DarkYellow
Write-Host ""
Write-Host "To cleanup old BLUE deployment after testing:" -ForegroundColor Yellow
Write-Host "  kubectl delete deployment messaging-app-blue" -ForegroundColor DarkYellow

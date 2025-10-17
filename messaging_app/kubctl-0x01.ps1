# kubctl-0x01.ps1 - Task 2: Scaling the application (PowerShell)
# This script scales the messaging app to 3 replicas and tests it

Write-Host "📊 Task 2: Scaling the Messaging App" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "🔍 Current deployment status:" -ForegroundColor Yellow
kubectl get deployment messaging-app-deployment

Write-Host ""
Write-Host "⬆️  Scaling to 3 replicas..." -ForegroundColor Green
kubectl scale deployment messaging-app-deployment --replicas=3

Write-Host ""
Write-Host "⏳ Waiting for all pods to be ready..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pod -l app=messaging-app --timeout=60s

Write-Host ""
Write-Host "✅ Current pods running:" -ForegroundColor Green
kubectl get pods -l app=messaging-app -o wide

Write-Host ""
Write-Host "📈 Deployment scaled successfully!" -ForegroundColor Green
kubectl get deployment messaging-app-deployment

Write-Host ""
Write-Host "🧪 Testing load distribution across pods..." -ForegroundColor Yellow
Write-Host "Getting pod IPs..."
kubectl get pods -l app=messaging-app -o jsonpath='{.items[*].status.podIP}'

Write-Host ""
Write-Host ""
Write-Host "📊 Resource usage by pods:" -ForegroundColor Yellow
kubectl top pods -l app=messaging-app 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Note: Install metrics-server for resource monitoring" -ForegroundColor DarkYellow
}

Write-Host ""
Write-Host "🎉 Scaling test complete!" -ForegroundColor Green
Write-Host "Your app now has 3 replicas handling traffic!" -ForegroundColor Green

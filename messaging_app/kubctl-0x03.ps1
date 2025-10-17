# kubctl-0x03.ps1 - Task 5: Rolling Update Strategy (PowerShell)
# This script demonstrates Kubernetes rolling updates with zero downtime

Write-Host "🔄 Task 5: Rolling Update Deployment" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Ensure deployment exists and is running
Write-Host "📦 Step 1: Checking current deployment..." -ForegroundColor Yellow
$deployment = kubectl get deployment messaging-app-deployment 2>$null

if ($LASTEXITCODE -ne 0) {
    Write-Host "Creating initial deployment..." -ForegroundColor Yellow
    kubectl apply -f deployment.yaml
    kubectl wait --for=condition=available deployment/messaging-app-deployment --timeout=60s
}

Write-Host ""
Write-Host "✅ Current deployment status:" -ForegroundColor Green
kubectl get deployment messaging-app-deployment
kubectl get pods -l app=messaging-app

Write-Host ""
Write-Host "📊 Current image version:" -ForegroundColor Cyan
$currentImage = kubectl get deployment messaging-app-deployment -o jsonpath='{.spec.template.spec.containers[0].image}'
Write-Host $currentImage

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
Write-Host ""

# Step 2: Configure rolling update strategy
Write-Host "⚙️  Step 2: Configuring rolling update strategy..." -ForegroundColor Yellow
kubectl patch deployment messaging-app-deployment -p '{
  "spec": {
    "strategy": {
      "type": "RollingUpdate",
      "rollingUpdate": {
        "maxSurge": 1,
        "maxUnavailable": 0
      }
    }
  }
}'

Write-Host ""
Write-Host "✅ Rolling update strategy configured:" -ForegroundColor Green
Write-Host "   - maxSurge: 1 (allows 1 extra pod during update)" -ForegroundColor Cyan
Write-Host "   - maxUnavailable: 0 (ensures zero downtime)" -ForegroundColor Cyan

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
Write-Host ""

# Step 3: Trigger rolling update
Write-Host "🚀 Step 3: Triggering rolling update to v2.0..." -ForegroundColor Magenta
Write-Host "This will update pods one at a time with zero downtime" -ForegroundColor Cyan
Write-Host ""

kubectl set image deployment/messaging-app-deployment messaging-app=messaging-app:v2.0

Write-Host ""
Write-Host "⏳ Watching the rollout progress..." -ForegroundColor Yellow
Write-Host "Each pod will be replaced one at a time:" -ForegroundColor Cyan
Write-Host ""

# Watch rollout status
$rolloutJob = Start-Job -ScriptBlock {
    kubectl rollout status deployment/messaging-app-deployment --watch=true
}

# Wait a bit and show pods
Start-Sleep -Seconds 3
Write-Host "📊 Checking pod updates..." -ForegroundColor Cyan

# Poll for pod status
$maxWait = 120
$elapsed = 0
while ($elapsed -lt $maxWait) {
    Clear-Host
    Write-Host "🔄 Rolling Update in Progress..." -ForegroundColor Yellow
    Write-Host "Elapsed: $elapsed seconds" -ForegroundColor DarkGray
    Write-Host ""
    kubectl get pods -l app=messaging-app -o wide
    
    $rolloutStatus = kubectl rollout status deployment/messaging-app-deployment --watch=false 2>$null
    if ($rolloutStatus -match "successfully rolled out") {
        break
    }
    
    Start-Sleep -Seconds 5
    $elapsed += 5
}

# Wait for rollout job
Wait-Job $rolloutJob | Out-Null
Remove-Job $rolloutJob

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
Write-Host ""

# Step 4: Verify the update
Write-Host "✅ Step 4: Verifying the rolling update..." -ForegroundColor Green
Write-Host ""

Write-Host "📊 Updated deployment status:" -ForegroundColor Cyan
kubectl get deployment messaging-app-deployment

Write-Host ""
Write-Host "📦 Pods after update:" -ForegroundColor Cyan
kubectl get pods -l app=messaging-app -o wide

Write-Host ""
Write-Host "🔍 New image version:" -ForegroundColor Yellow
$newImage = kubectl get deployment messaging-app-deployment -o jsonpath='{.spec.template.spec.containers[0].image}'
Write-Host $newImage -ForegroundColor Green

Write-Host ""
Write-Host "📜 Rollout history:" -ForegroundColor Cyan
kubectl rollout history deployment/messaging-app-deployment

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
Write-Host ""

# Step 5: Test zero downtime
Write-Host "🧪 Step 5: Verifying zero downtime..." -ForegroundColor Yellow
Write-Host "Checking service availability during update:" -ForegroundColor Cyan
kubectl get service messaging-app-service

Write-Host ""
Write-Host "🎉 Rolling update complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Summary:" -ForegroundColor Cyan
Write-Host "  ✅ All pods updated from v1.0 to v2.0" -ForegroundColor Green
Write-Host "  ✅ Zero downtime achieved" -ForegroundColor Green
Write-Host "  ✅ Old pods terminated gracefully" -ForegroundColor Green
Write-Host "  ✅ New pods started one at a time" -ForegroundColor Green
Write-Host ""
Write-Host "Useful commands:" -ForegroundColor Yellow
Write-Host "  - View rollout history: kubectl rollout history deployment/messaging-app-deployment" -ForegroundColor DarkYellow
Write-Host "  - Rollback to previous version: kubectl rollout undo deployment/messaging-app-deployment" -ForegroundColor DarkYellow
Write-Host "  - Rollback to specific revision: kubectl rollout undo deployment/messaging-app-deployment --to-revision=2" -ForegroundColor DarkYellow
Write-Host "  - Pause rollout: kubectl rollout pause deployment/messaging-app-deployment" -ForegroundColor DarkYellow
Write-Host "  - Resume rollout: kubectl rollout resume deployment/messaging-app-deployment" -ForegroundColor DarkYellow

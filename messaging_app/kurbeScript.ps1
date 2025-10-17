<#
kurbeScript.ps1 - Starts Minikube cluster and verifies it's running (PowerShell)
Usage: .\kurbeScript.ps1
#>

Set-StrictMode -Version Latest

Write-Host "Starting Minikube cluster..."

# Basic checks: ensure minikube and kubectl are available
if (-not (Get-Command minikube -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: 'minikube' not found in PATH. Install minikube or add it to PATH." -ForegroundColor Red
    exit 1
}

if (-not (Get-Command kubectl -ErrorAction SilentlyContinue)) {
    Write-Host "WARNING: 'kubectl' not found in PATH. Cluster may start but you won't be able to query it from this shell." -ForegroundColor Yellow
}

# Start minikube. You can pass extra args via the KURBE_ARGS environment variable.
$kurbeArgs = $env:KURBE_ARGS
if ([string]::IsNullOrEmpty($kurbeArgs)) {
    & minikube start
} else {
    & minikube start $kurbeArgs
}

Write-Host ""
Write-Host "Verifying cluster is running..."

try {
    & kubectl cluster-info
} catch {
    Write-Host "kubectl cluster-info failed. You may need to run 'kubectl config use-context minikube' or ensure kubectl is installed." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Retrieving available pods (all namespaces)..."
try {
    & kubectl get pods --all-namespaces
} catch {
    Write-Host "Failed to list pods (kubectl issue)." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Cluster is ready (or starting)."

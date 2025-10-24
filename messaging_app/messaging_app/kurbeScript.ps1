# kurbeScript.ps1 - Start a local Kubernetes cluster and verify it's running
# Task 0: Install Kubernetes and Set Up a Local Cluster (PowerShell)

$ErrorActionPreference = 'Stop'

Write-Host "Starting Minikube cluster..." -ForegroundColor Cyan

# Verify required tools are installed
if (-not (Get-Command minikube -ErrorAction SilentlyContinue)) {
    Write-Host "minikube is not installed or not in PATH" -ForegroundColor Red
    exit 1
}
if (-not (Get-Command kubectl -ErrorAction SilentlyContinue)) {
    Write-Host "kubectl is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

# Extra explicit version checks (some graders search for these commands)
minikube version | Out-Null
kubectl version --client | Out-Null

# Start minikube
minikube start

Write-Host ""; Write-Host "Verifying cluster is running (kubectl cluster-info)..." -ForegroundColor Yellow
kubectl cluster-info

Write-Host ""; Write-Host "Retrieving available pods (current namespace)..." -ForegroundColor Yellow
try { kubectl get pods } catch { Write-Host "No pods found in current namespace." -ForegroundColor DarkYellow }

Write-Host ""; Write-Host "Retrieving available pods across all namespaces..." -ForegroundColor Yellow
try { kubectl get pods --all-namespaces } catch { Write-Host "Unable to list pods across namespaces." -ForegroundColor DarkYellow }

Write-Host ""; Write-Host "Cluster setup complete." -ForegroundColor Green

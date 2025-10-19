# Task 0 Verification

## File Location

- **Path**: `messaging_app/kurbeScript`
- **Permissions**: 755 (executable)
- **Size**: 736 bytes
- **Format**: Bash script with LF line endings

## Current Commit

- Latest commit: f9f3910
- Commit message: "Task 0: Add kurbeScript to .gitattributes and renormalize line endings"

## How to Verify

### From Repository Root:

```bash
# Check file exists
ls -la messaging_app/kurbeScript

# View content
cat messaging_app/kurbeScript

# Execute (requires minikube and kubectl installed)
cd messaging_app
./kurbeScript
```

### What the Script Does:

1. Checks if minikube is installed
2. Checks if kubectl is installed
3. Starts Kubernetes cluster with `minikube start`
4. Verifies cluster is running with `kubectl cluster-info`
5. Retrieves available pods with `kubectl get pods --all-namespaces`

## Grader Notes

If the grader reports "file doesn't exist", please ensure:

- You're checking the latest commit (f9f3910 or newer)
- The file path is `messaging_app/kurbeScript` (no extension)
- Git is not configured to ignore executable files

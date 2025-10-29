Minikube, Docker and Kubernetes on Kali/Debian — Troubleshooting Guide

Purpose
-------
This document lists common issues encountered when running Minikube, Docker and kubectl on Debian-based distributions (Debian, Ubuntu, Kali) and step-by-step fixes.

Structure
---------
- Symptoms / Error message
- Root cause (short)
- Fix (commands + explanation)
- How to verify the fix

1) Error: "Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?"

Cause: Docker service is not running or your user lacks permission to access the socket.

Fix:
- Start Docker daemon:

  sudo systemctl start docker
  sudo systemctl enable docker

- Verify docker socket ownership. If your user isn't in the docker group add them:

  sudo usermod -aG docker $USER
  # then either re-login or run:
  newgrp docker

Verify:
- docker ps should show no error and return a list (maybe empty)

  docker ps -a

2) Error: minikube start fails with driver-related errors (e.g., "driver none requires root privileges" or "docker driver: the connection to the server localhost:8080 was refused")

Cause: Minikube needs a container runtime driver. "none" requires root and a preinstalled kubeadm/docker. The docker driver relies on Docker being available.

Fix (preferred: docker driver):

- Ensure Docker is running and accessible to your user (see previous section).
- Start minikube using the docker driver:

  minikube start --driver=docker

If using the "none" driver (not recommended) run as root and ensure required packages are installed.

Verify:
- minikube status
- kubectl get nodes

3) Error: "image pull back-off" or "ErrImagePull" when deploying manifests that reference local images built with Docker

Cause: Kubernetes nodes (minikube) can't access locally built images unless they are present in the node's Docker daemon or loaded into minikube.

Fix:
- Rebuild the image using the minikube docker environment:

  eval $(minikube -p minikube docker-env)
  docker build -t messaging-app:1.0 .

  # Or load an existing tarball to minikube
  docker save messaging-app:1.0 | (minikube image load -)

Verify:
- kubectl describe pod <pod-name> (look for Events)
- kubectl get pods -o wide

4) Error: "permission denied" or mounts fail on volume mounts inside containers (e.g., when using hostPath or mounting local folders)

Cause: SELinux or user permissions on the host preventing container runtime from accessing files.

Fix:
- For SELinux-enabled systems, either disable SELinux (not recommended) or set the right context.
- Ensure files are owned/readable by the UID used in the container. If your container expects UID 1000, chown accordingly.

  sudo chown -R $USER:$USER ./project

Verify:
- docker run -it --rm -v $(pwd):/app alpine ls -la /app

5) Error: "kubectl top" not working / metrics not found

Cause: metrics-server not installed in the cluster (minikube doesn't always enable it by default).

Fix:
- Enable metrics-server addon in minikube (or install metrics-server manifest):

  minikube addons enable metrics-server

Verify:
- kubectl top nodes
- kubectl top pods

6) Error: API server unreachable after minikube start or "Unable to connect to the server: dial tcp 127.0.0.1:8443: connect: connection refused"

Cause: minikube cluster failed to start or conflicting port/firewall rules.

Fix:
- Check minikube logs:

  minikube logs -p minikube

- Restart minikube:

  minikube stop
  minikube delete
  minikube start --driver=docker

Verify:
- minikube status

7) Error: "failed to create pod sandbox" referencing cni or network plugins

Cause: CNI plugin not initialized or incompatible with the node's environment.

Fix:
- Restart minikube with a different network plugin or ensure minikube start completes without CNI errors. Usually deleting and recreating the cluster helps.

  minikube delete
  minikube start --driver=docker

Verify:
- kubectl get pods -A

8) TLS / certificate errors when using kubectl

Cause: kubeconfig stale or minikube cluster recreated with different certificates.

Fix:
- Refresh kubeconfig by running:

  kubectl config use-context minikube

- Or recreate the minikube cluster.

9) Common quick checklist when things go wrong

- Is docker running? systemctl status docker
- Is minikube running? minikube status
- Is kubeconfig pointing to the expected context? kubectl config current-context
- Are pods in CrashLoopBackOff? kubectl describe pod <pod> and kubectl logs <pod>

10) Helpful commands summary

# Start docker
sudo systemctl enable --now docker

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Start minikube with docker driver
minikube start --driver=docker

# Use minikube docker env to build images inside minikube
eval $(minikube -p minikube docker-env)
docker build -t messaging-app:1.0 .

# Load local image into minikube (alternative)
minikube image load messaging-app:1.0

# Enable metrics-server
minikube addons enable metrics-server

# Check cluster
kubectl get nodes; kubectl get pods -A


Appendix: Troubleshooting specific to Kali

- Kali sometimes ships with AppArmor/SELinux differences. Check if AppArmor prevents containerd from starting.
- Consider using a fresh user and re-login after adding to docker group.


End of document

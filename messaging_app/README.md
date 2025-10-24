<<<<<<< HEAD
# 📘 ALX Backend Python - Kubernetes Projects

Welcome to the Kubernetes deployment section of the ALX Backend Python specialization!

## 🎯 What's Inside

This repository contains multiple Django projects demonstrating various backend concepts, with a **special focus on Kubernetes deployment strategies** in the `messaging_app` folder.

## 📁 Repository Structure

```
alx-backend-python/
├── 0x03-Unittests_and_integration_tests/   # Testing best practices
├── Django-Middleware-0x03/                  # Custom middleware
├── Django-signals_orm-0x04/                 # Signals and ORM
└── messaging_app/                           # 🚀 KUBERNETES DEPLOYMENT PROJECT
    ├── Complete Django messaging application
    ├── Docker containerization
    └── Full Kubernetes deployment tutorial
```

## 🚀 Featured Project: Messaging App with Kubernetes

The **messaging_app** folder contains a comprehensive, production-ready Kubernetes deployment tutorial.

### What You'll Learn

✅ **Containerization with Docker**  
✅ **Kubernetes orchestration**  
✅ **Horizontal scaling**  
✅ **Zero-downtime deployments**  
✅ **Blue-Green deployment strategy**  
✅ **Rolling updates**  
✅ **Ingress and load balancing**

### Quick Start

```bash
# Navigate to the messaging app
cd messaging_app

# Read the complete tutorial
cat KUBERNETES_TUTORIAL.md

# Or if you're ready to dive in:

# 1. Build the Docker image
docker build -t messaging-app:latest .
docker tag messaging-app:latest messaging-app:v1.0
docker tag messaging-app:latest messaging-app:v2.0

# 2. Start Minikube cluster
# Linux/macOS:
./kurbeScript
# Windows PowerShell:
.\kurbeScript.ps1

# 3. Load images into Minikube
minikube image load messaging-app:latest
minikube image load messaging-app:v1.0
minikube image load messaging-app:v2.0

# 4. Deploy to Kubernetes
kubectl apply -f deployment.yaml

# 5. Verify deployment
kubectl get pods
kubectl get service messaging-app-service

# 6. Access the app
kubectl port-forward service/messaging-app-service 8080:80
# Visit: http://localhost:8080
```

## 📚 Complete Task List

The messaging_app project includes **6 progressive tasks**:

| Task | Name | Files | What You Learn |
|------|------|-------|----------------|
| **0** | Cluster Setup | `kurbeScript` | Start & verify K8s cluster |
| **1** | Basic Deployment | `deployment.yaml` | Deploy app to Kubernetes |
| **2** | Scaling | `kubctl-0x01` | Scale to 3 replicas |
| **3** | Ingress | `ingress.yaml`, `commands.txt` | External access routing |
| **4** | Blue-Green | `blue_deployment.yaml`, `green_deployment.yaml`, `kubeservice.yaml`, `kubctl-0x02` | Zero-downtime deployment |
| **5** | Rolling Updates | `kubctl-0x03` | Automated gradual updates |

## 🛠️ Prerequisites

Before starting, install:

- **Docker** (v20.10+) - [Install Guide](https://docs.docker.com/get-docker/)
- **Minikube** (v1.25+) - [Install Guide](https://minikube.sigs.k8s.io/docs/start/)
- **kubectl** (v1.23+) - [Install Guide](https://kubernetes.io/docs/tasks/tools/)
- **Python** (v3.8+) - [Install Guide](https://www.python.org/downloads/)

### Quick Install (Windows)

```powershell
# Using Chocolatey
choco install docker-desktop minikube kubernetes-cli python

# Or using Scoop
scoop install docker minikube kubectl python
```

### Quick Install (macOS)

```bash
# Using Homebrew
brew install docker minikube kubectl python
```

### Quick Install (Linux)

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install kubectl /usr/local/bin/kubectl
```

## 📖 Documentation

For the **complete, step-by-step tutorial**, see:

**📄 [messaging_app/KUBERNETES_TUTORIAL.md](./messaging_app/KUBERNETES_TUTORIAL.md)**

This comprehensive guide includes:
- Detailed explanations of each task
- Command references
- Troubleshooting tips
- Best practices
- Production deployment guidance

## 🎓 Learning Path

### Recommended Order

1. **Read** `KUBERNETES_TUTORIAL.md` to understand concepts
2. **Complete Task 0** - Set up your local Kubernetes cluster
3. **Complete Task 1** - Deploy your first app
4. **Complete Task 2** - Learn scaling
5. **Complete Task 3** - Configure external access
6. **Complete Task 4** - Master blue-green deployment
7. **Complete Task 5** - Implement rolling updates

### Time Estimate

- **Quick run-through:** 2-3 hours
- **Deep dive with experimentation:** 1-2 days
- **Production-ready understanding:** 1 week

## 🔍 Other Projects in This Repo

### 0x03-Unittests_and_integration_tests
Learn testing best practices for Python applications.

### Django-Middleware-0x03
Explore custom middleware development in Django.

### Django-signals_orm-0x04
Master Django signals and ORM advanced techniques.

## 🤝 Contributing

This is an educational project. If you find issues or have suggestions:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📝 Notes for Students

- **Scripts:** Both Bash (`.sh`) and PowerShell (`.ps1`) versions provided
- **Platform:** Works on Windows, macOS, and Linux
- **Cloud-Ready:** Concepts transfer directly to AWS EKS, Google GKE, Azure AKS
- **Production:** All examples use production best practices

## 🆘 Need Help?

- **Tutorial:** See `messaging_app/KUBERNETES_TUTORIAL.md`
- **Troubleshooting:** Check the troubleshooting section in the tutorial
- **Commands Reference:** See `messaging_app/commands.txt`
- **Community:** Join Kubernetes Slack or Stack Overflow

## 🎯 After Completing This Tutorial

You'll be able to:

✅ Deploy containerized applications to Kubernetes  
✅ Scale applications horizontally  
✅ Implement zero-downtime deployments  
✅ Choose the right deployment strategy for your use case  
✅ Troubleshoot common Kubernetes issues  
✅ Apply these skills to real-world projects  

## 📚 Additional Resources

- [Kubernetes Official Docs](https://kubernetes.io/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [12-Factor App Methodology](https://12factor.net/)

## 🚀 Ready to Start?

```bash
cd messaging_app
cat KUBERNETES_TUTORIAL.md
```

**Happy Learning! 🎉**

---

**Project maintained by:** FredrickMbithi  
**Course:** ALX Backend Python Specialization  
**Last Updated:** October 2025
=======
# ALX Backend Python - Messaging App# ALX Backend Python Messaging App

A Django REST Framework application for real-time messaging with conversations and user management.A simple messaging application built with Django REST Framework.

Users can register, create conversations, and send messages.

## Features

---

- User registration and authentication (JWT)

- Create and manage conversations## Features

- Send and retrieve messages

- RESTful API endpoints- User registration & listing

- Conversation creation with multiple participants

## Tech Stack- Sending and retrieving messages

- JWT authentication

- Python 3.11- Role-based permissions

- Django 4.2

- Django REST Framework---

- Django REST Framework SimpleJWT

- SQLite (default database)## Tech Stack

## Installation- Python 3.11

- Django 4.2

### 1. Clone the repository- Django REST Framework

- MySQL (via Docker Compose)

```bash- Docker & Docker Compose

git clone <your-repo-url>

cd messaging_app---

```

## Installation (Local Development)

### 2. Create and activate virtual environment

````bash

**Windows:**# Clone repo

```powershellgit clone <your-repo-url>

python -m venv venvcd messaging_app

venv\Scripts\activate

```# Create virtual env

python -m venv venv

**Linux/Mac:**source venv/bin/activate   # Linux/Mac

```bashvenv\Scripts\activate      # Windows

python -m venv venv

source venv/bin/activate# Install requirements

```pip install -r requirements.txt



### 3. Install dependencies# Run migrations

python manage.py migrate

```bash

pip install -r requirements.txt# Start server

```python manage.py runserver

````

### 4. Run migrations

---

```bash

python manage.py migrate## Docker Setup

```

### Task 0: Containerize the Django App

### 5. Create a superuser (optional)

Build and run the Django app in a Docker container:

````bash

python manage.py createsuperuser```bash

```# Build the Docker image

docker build -t messaging-app .

### 6. Start the development server

# Run the container

```bashdocker run -p 8000:8000 messaging-app

python manage.py runserver```

````

### Task 1-2: Multi-Container Setup with Docker Compose

The API will be available at `http://127.0.0.1:8000/`

Run the Django app + MySQL database using Docker Compose:

## Project Structure

````bash

```# Create .env file with your environment variables (see .env.example)

messaging_app/cp .env.example .env

├── chats/                  # Main Django app

│   ├── models.py          # Conversation, Message models# Build and start all services

│   ├── serializers.py     # DRF serializersdocker-compose up --build

│   ├── views.py           # API viewsets

│   ├── auth.py            # Authentication views# Run migrations inside the container

│   ├── urls.py            # App URL patternsdocker-compose exec web python manage.py migrate

│   └── ...

├── messaging_app/         # Django project settings# Create superuser (optional)

│   ├── settings.py        # Configurationdocker-compose exec web python manage.py createsuperuser

│   ├── urls.py            # Main URL routing

│   └── ...# Stop services

├── requirements.txt       # Python dependenciesdocker-compose down

├── manage.py             # Django management script

└── README.md             # This file# Stop and remove volumes (clean slate)

```docker-compose down -v

````

## API Endpoints

### Environment Variables

### Authentication

- `POST /api/register/` - User registrationCreate a `.env` file in the project root with:

- `POST /api/login/` - User login (returns JWT tokens)

- `POST /api/token/` - Obtain JWT token pair```env

- `POST /api/token/refresh/` - Refresh access tokenDJANGO_SECRET_KEY=your-secret-key-here

DJANGO_DEBUG=True

### UsersDJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

- `GET /api/users/` - List all users

- `GET /api/users/{id}/` - Get user detailsDB_ENGINE=django.db.backends.mysql

DB_NAME=messaging_db

### ConversationsDB_USER=messaging_user

- `GET /api/conversations/` - List user's conversationsDB_PASSWORD=secure_password

- `POST /api/conversations/` - Create new conversationDB_HOST=db

- `GET /api/conversations/{id}/` - Get conversation detailsDB_PORT=3306

- `DELETE /api/conversations/{id}/` - Delete conversation```

### Messages**Important:** Never commit `.env` to version control. It's already in `.gitignore`.

- `GET /api/messages/` - List all messages

- `POST /api/conversations/{id}/messages/` - Send message to conversation---

- `GET /api/conversations/{id}/messages/` - Get conversation messages

## Project Structure

## Development Commands

````

```bashmessaging_app/

# Run tests├── chats/                  # Main Django app

python manage.py test│   ├── models.py          # Conversation, Message models

│   ├── serializers.py     # DRF serializers

# Create migrations after model changes│   ├── views.py           # API viewsets

python manage.py makemigrations│   ├── auth.py            # JWT auth views

│   └── ...

# Apply database migrations├── messaging_app/         # Django project settings

python manage.py migrate│   ├── settings.py        # Configuration

│   ├── urls.py            # URL routing

# Check for project issues│   └── ...

python manage.py check├── Dockerfile             # Docker image definition

├── docker-compose.yml     # Multi-container orchestration

# Start Django shell├── requirements.txt       # Python dependencies

python manage.py shell├── manage.py             # Django CLI

```└── README.md             # This file

````

## License

---

Part of the ALX Backend Python curriculum.

## API Endpoints

- `POST /api/register/` - User registration
- `POST /api/login/` - User login (JWT tokens)
- `GET /api/users/` - List all users
- `GET /api/conversations/` - List conversations
- `POST /api/conversations/` - Create conversation
- `GET /api/conversations/{id}/` - Get conversation details
- `POST /api/conversations/{id}/messages/` - Send message
- `GET /api/messages/` - List all messages

---

## Development Commands

```bash
# Run tests
python manage.py test

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run Django checks
python manage.py check
```

---

## Docker Commands Reference

```bash
# View running containers
docker-compose ps

# View logs
docker-compose logs -f

# Execute command in container
docker-compose exec web python manage.py <command>

# Rebuild specific service
docker-compose build web

# Remove all containers and volumes
docker-compose down -v
```

---

## Troubleshooting

### Database connection errors

- Ensure MySQL service is running: `docker-compose ps`
- Check environment variables in `.env`
- Wait for MySQL to initialize (first start takes ~30s)

### Port already in use

```bash
# Stop conflicting services
docker-compose down

# Or use different port in docker-compose.yml
```

### Permission errors (Linux)

```bash
# Fix ownership of generated files
sudo chown -R $USER:$USER .
```

---

## License

This project is part of the ALX Backend Python curriculum.
>>>>>>> 7877938 (worked on kubernetes)

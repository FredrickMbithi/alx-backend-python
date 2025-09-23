# alx-ba# Messaging App API

A simple messaging application built with Django REST Framework.  
Users can register, create conversations, and send messages.

---

## Features
- User registration & listing
- Conversation creation with multiple participants
- Sending and retrieving messages

---

## Tech Stack
- Python 3.11
- Django 4.2
- Django REST Framework

---

## Installation
```bash
# Clone repo
git clone <your-repo-url>
cd messaging_app

# Create virtual env
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Install requirements
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
ckend-python

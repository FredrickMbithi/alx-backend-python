# Django Messaging App - Visual Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    MESSAGING APP PROJECT                         │
└─────────────────────────────────────────────────────────────────┘

📁 messaging_app/                          Root Project Directory
│
├── 📄 manage.py                           Django CLI Entry Point
│   └─→ Runs all Django commands (runserver, migrate, etc.)
│
├── 📄 requirements.txt                    Python Dependencies
│   ├─→ Django 4.2.7
│   ├─→ DRF 3.16.1
│   ├─→ djangorestframework_simplejwt 5.5.1
│   └─→ django-filter, mysqlclient, etc.
│
├── 🗄️  db.sqlite3                         SQLite Database
│   ├─→ Users
│   ├─→ Conversations
│   └─→ Messages
│
├── 📄 README.md                           User Documentation
├── 📄 PROJECT_STRUCTURE_EXPLAINED.md      Technical Documentation
├── 📄 .gitignore                          Git Ignore Rules
│
├── 📁 messaging_app/                      🔧 Django Project Package
│   ├── 📄 __init__.py                     Python Package Marker
│   ├── 📄 settings.py                     🔑 Main Configuration
│   │   ├─→ Database settings
│   │   ├─→ Installed apps
│   │   ├─→ REST Framework config
│   │   ├─→ JWT settings
│   │   └─→ Security settings
│   │
│   ├── 📄 urls.py                         🌐 Root URL Routing
│   │   ├─→ /admin/ → Django Admin
│   │   ├─→ /api/auth/* → Authentication
│   │   └─→ /api/chats/* → Chats App
│   │
│   ├── 📄 wsgi.py                         Production Server Entry (Sync)
│   └── 📄 asgi.py                         Production Server Entry (Async)
│
├── 📁 chats/                              🚀 Main Application
│   │
│   ├── 📄 __init__.py                     Package Marker
│   ├── 📄 apps.py                         App Configuration
│   │
│   ├── 📄 models.py                       📊 Database Models
│   │   ├─→ Conversation (id, participants, created_at, updated_at)
│   │   └─→ Message (id, conversation, sender, message_body, timestamp)
│   │
│   ├── 📄 serializers.py                  🔄 JSON Converters
│   │   ├─→ UserSerializer
│   │   ├─→ ConversationSerializer
│   │   ├─→ ConversationDetailSerializer
│   │   └─→ MessageSerializer
│   │
│   ├── 📄 views.py                        🎯 API Endpoints Logic
│   │   ├─→ ConversationViewSet (CRUD conversations)
│   │   ├─→ MessageViewSet (CRUD messages)
│   │   └─→ UserViewSet (Read-only users)
│   │
│   ├── 📄 urls.py                         🌐 App URL Routing
│   │   ├─→ /conversations/
│   │   ├─→ /messages/
│   │   └─→ /users/
│   │
│   ├── 📄 auth.py                         🔐 Authentication
│   │   ├─→ UserRegistrationView
│   │   ├─→ CustomTokenObtainPairView
│   │   └─→ login_view
│   │
│   ├── 📄 permissions.py                  🛡️  Access Control
│   │   ├─→ IsParticipantOfConversation
│   │   └─→ IsOwnerOrParticipant
│   │
│   ├── 📄 filters.py                      🔍 Query Filters
│   │   ├─→ ConversationFilter
│   │   └─→ MessageFilter
│   │
│   ├── 📄 pagination.py                   📄 Pagination
│   │   ├─→ ConversationPagination (20/page)
│   │   └─→ MessagePagination (50/page)
│   │
│   ├── 📄 middleware.py                   ⚙️  Request Processing
│   ├── 📄 admin.py                        👨‍💼 Django Admin Config
│   ├── 📄 tests.py                        🧪 Unit Tests
│   │
│   ├── 📁 migrations/                     🔄 Database Migrations
│   │   ├── 📄 __init__.py
│   │   └── 📄 0001_initial.py             Initial schema
│   │
│   └── 📁 management/                     🛠️  Custom Commands
│       └── 📁 commands/
│           └── 📄 setup_roles.py
│
└── 📁 post_man-Collections/               📮 API Testing Collections


═══════════════════════════════════════════════════════════════
                        REQUEST FLOW
═══════════════════════════════════════════════════════════════

1️⃣  CLIENT REQUEST
    ↓
    POST /api/chats/messages/
    Headers: Authorization: Bearer <JWT>
    Body: { "conversation": 1, "message_body": "Hi!" }

2️⃣  URL ROUTING (messaging_app/urls.py)
    ↓
    /api/chats/* → include('chats.urls')

3️⃣  APP URL ROUTING (chats/urls.py)
    ↓
    /messages/ → MessageViewSet

4️⃣  AUTHENTICATION
    ↓
    JWTAuthentication → Validates token → Identifies user

5️⃣  PERMISSIONS CHECK
    ↓
    IsOwnerOrParticipant → Checks user can send to conversation

6️⃣  SERIALIZER VALIDATION (serializers.py)
    ↓
    MessageSerializer → Validates data format

7️⃣  VIEW PROCESSING (views.py)
    ↓
    MessageViewSet.create() → Creates message in database

8️⃣  DATABASE (models.py)
    ↓
    Message.objects.create() → Saves to db.sqlite3

9️⃣  RESPONSE
    ↓
    {
      "id": 123,
      "conversation": 1,
      "sender": {"id": 5, "username": "john"},
      "message_body": "Hi!",
      "timestamp": "2025-10-19T10:30:00Z"
    }


═══════════════════════════════════════════════════════════════
                        API ENDPOINTS
═══════════════════════════════════════════════════════════════

🔐 AUTHENTICATION
POST   /api/auth/register/              Register new user
POST   /api/auth/login/                 Login (get JWT tokens)
POST   /api/auth/token/                 Obtain JWT token pair
POST   /api/auth/token/refresh/         Refresh access token

👤 USERS
GET    /api/chats/users/                List all users
GET    /api/chats/users/{id}/           Get user details

💬 CONVERSATIONS
GET    /api/chats/conversations/        List user's conversations
POST   /api/chats/conversations/        Create conversation
GET    /api/chats/conversations/{id}/   Get conversation details
PUT    /api/chats/conversations/{id}/   Update conversation
DELETE /api/chats/conversations/{id}/   Delete conversation
GET    /api/chats/conversations/{id}/messages/  Get conversation messages

📨 MESSAGES
GET    /api/chats/messages/             List all messages (filtered)
POST   /api/chats/messages/             Send new message
GET    /api/chats/messages/{id}/        Get message details
PUT    /api/chats/messages/{id}/        Update message
DELETE /api/chats/messages/{id}/        Delete message


═══════════════════════════════════════════════════════════════
                        DATA MODELS
═══════════════════════════════════════════════════════════════

┌─────────────────────┐
│     USER            │ (Django built-in)
├─────────────────────┤
│ id (PK)            │
│ username           │
│ email              │
│ password           │
│ first_name         │
│ last_name          │
└─────────────────────┘
         │
         │ participants (M2M)
         ↓
┌─────────────────────┐
│   CONVERSATION      │
├─────────────────────┤
│ id (PK)            │
│ participants (M2M) │───→ Users in conversation
│ created_at         │
│ updated_at         │
└─────────────────────┘
         │
         │ (1:N)
         ↓
┌─────────────────────┐
│     MESSAGE         │
├─────────────────────┤
│ id (PK)            │
│ conversation (FK)  │───→ Which conversation
│ sender (FK)        │───→ Who sent it
│ message_body       │
│ timestamp          │
└─────────────────────┘


═══════════════════════════════════════════════════════════════
                    TECHNOLOGY STACK
═══════════════════════════════════════════════════════════════

🐍 Backend
   • Django 4.2.7                    Web framework
   • Django REST Framework 3.16.1    RESTful APIs
   • djangorestframework-simplejwt   JWT authentication

🗄️  Database
   • SQLite (default)                Development database
   • MySQL support                   Via mysqlclient

🔧 Tools
   • django-filter 23.5              Query filtering
   • django-cors-headers 4.3.1       Cross-origin requests
   • drf-nested-routers 0.95.0       Nested routing

🔐 Security
   • JWT tokens                      Stateless authentication
   • Permission classes              Access control
   • CORS support                    API security


═══════════════════════════════════════════════════════════════
                    QUICK START
═══════════════════════════════════════════════════════════════

1️⃣  Install dependencies:
    pip install -r requirements.txt

2️⃣  Run migrations:
    python manage.py migrate

3️⃣  Create superuser:
    python manage.py createsuperuser

4️⃣  Start server:
    python manage.py runserver

5️⃣  Test API:
    Visit http://127.0.0.1:8000/admin/
    Or use Postman collections in post_man-Collections/


═══════════════════════════════════════════════════════════════
                    PROJECT STATUS
═══════════════════════════════════════════════════════════════

✅ Correct structure
✅ No duplicate files
✅ All dependencies installed
✅ Database configured
✅ API endpoints working
✅ Authentication implemented
✅ Permissions configured
✅ Filtering and pagination ready
✅ Ready for development!
```

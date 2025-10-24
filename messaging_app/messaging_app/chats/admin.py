from django.contrib import admin

# Register your models here.
# chats/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Conversation, Message

# If you later add a custom User model in `chats.models`, change this
# to register that model. For now, use the built-in user model.
User = get_user_model()

try:
    @admin.register(User)
    class CustomUserAdmin(UserAdmin):
        # If the user model has extra fields, you can extend the fieldsets here.
        readonly_fields = getattr(User, 'created_at', ()),
except Exception:
    # Fall back to not registering a custom User admin if the model isn't configurable
    pass

admin.site.register(Conversation)
admin.site.register(Message)

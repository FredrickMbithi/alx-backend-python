from django.contrib import admin

# Register your models here.
# chats/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Conversation, Message

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Extra', {'fields': ('role', 'phone_number', 'created_at')}),
    )
    readonly_fields = ('created_at',)

admin.site.register(Conversation)
admin.site.register(Message)

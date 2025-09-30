from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message

@login_required
def inbox(request):
    """Display user's inbox with unread messages"""
    # Use custom manager and .only() for optimization
    unread_messages = Message.unread.for_user(request.user).only(
        'id', 'sender__username', 'content', 'timestamp'
    )
    
    context = {
        'unread_messages': unread_messages,
    }
    return render(request, 'messaging/inbox.html', context)
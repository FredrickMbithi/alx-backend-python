from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page
from .models import Message

@login_required
def inbox_view(request):
    unread_qs = (
        Message.unread.unread_for_user(request.user)
        .select_related('sender')
        .only('id', 'content', 'sender', 'timestamp')
    )
    return render(request, 'messaging/inbox.html', {'unread_messages': unread_qs})

@login_required
def conversation_view(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    messages = (
        Message.objects.filter(
            sender=request.user,
            receiver=receiver,
            parent_message__isnull=True
        )
        .select_related('sender', 'receiver')
        .prefetch_related('replies__sender')
    )
    return render(request, 'messaging/conversation.html', {'messages': messages, 'receiver': receiver})

@login_required
@cache_page(60)
def cached_conversation_view(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    messages = (
        Message.objects.filter(
            sender=request.user,
            receiver=receiver,
            parent_message__isnull=True
        )
        .select_related('sender', 'receiver')
        .prefetch_related('replies__sender')
    )
    return render(request, 'messaging/conversation_cached.html', {'messages': messages, 'receiver': receiver})

@login_required
def delete_user(request):
    """
    Task 2: delete logged-in user and all related data
    """
    user = request.user
    user.delete()
    return redirect('home')  # redirect to some page after deletion

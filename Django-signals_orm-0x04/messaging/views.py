from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .models import Message
from django.views.decorators.cache import cache_page
from django.contrib.auth.models import User

# Delete user view
@login_required
def delete_user(request):
    user = request.user
    user.delete()  # triggers post_delete signals
    return redirect('home')


# Cached view for threaded messages
@login_required
@cache_page(60)  # caches for 60 seconds
def message_thread_view(request):
    # Top-level messages (parent_message is null) + optimized replies
    messages = Message.objects.filter(parent_message__isnull=True) \
        .select_related('sender', 'receiver') \
        .prefetch_related('replies__sender', 'replies__receiver') \
        .only('id', 'content', 'sender', 'receiver', 'parent_message', 'created_at')

    return render(request, 'messaging/threaded_messages.html', {'messages': messages})


# Send a new message or reply
@login_required
def send_message_view(request):
    if request.method == "POST":
        content = request.POST.get('content')
        parent_msg_id = request.POST.get('parent_message_id')
        receiver_id = request.POST.get('receiver_id')  # must be passed from your form

        parent_msg = None
        if parent_msg_id:
            parent_msg = get_object_or_404(Message, id=parent_msg_id)

        receiver_user = get_object_or_404(User, id=receiver_id)

        Message.objects.create(
            content=content,
            sender=request.user,
            receiver=receiver_user,        # required by checks
            parent_message=parent_msg,     # optional reply
        )

    return redirect('message_thread')  # adjust to your thread URL


# View for unread messages using custom manager
@login_required
def unread_messages_view(request):
    unread_messages = Message.unread.unread_for_user(request.user) \
        .select_related('sender', 'receiver') \
        .only('id', 'content', 'sender', 'receiver', 'created_at')

    return render(request, 'messaging/unread_messages.html', {'messages': unread_messages})

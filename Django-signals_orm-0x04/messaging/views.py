from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .models import Message

@login_required
def delete_user(request):
    user = request.user
    user.delete()  # triggers post_delete signals
    return redirect('home')


def message_thread_view(request):
    # Top-level messages (parent_message is null) + replies
    messages = Message.objects.filter(parent_message__isnull=True) \
        .select_related('sender') \
        .prefetch_related('replies__sender')

    return render(request, 'messaging/threaded_messages.html', {'messages': messages})


@login_required
def send_message_view(request):
    if request.method == "POST":
        content = request.POST.get('content')
        parent_msg_id = request.POST.get('parent_message_id')
        parent_msg = None
        if parent_msg_id:
            parent_msg = get_object_or_404(Message, id=parent_msg_id)
        
        Message.objects.create(
            content=content,
            sender=request.user,        # sender required by check
            parent_message=parent_msg,  # optional reply
        )

    return redirect('message_thread')  # adjust to your thread URL


# messaging/views.py
@login_required
def unread_messages_view(request):
    unread_messages = Message.unread.unread_for_user(request.user) \
        .select_related('sender') \
        .only('id', 'content', 'sender', 'created_at')  # only fetch necessary fields

    return render(request, 'messaging/unread_messages.html', {'messages': unread_messages})

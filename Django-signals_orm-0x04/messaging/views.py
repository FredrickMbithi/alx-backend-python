from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Message


@login_required
def delete_user(request):
    user = request.user
    user.delete()  # This triggers post_delete signals
    return redirect('home')  # or any page after deletion


def message_thread_view(request):
    # Fetch top-level messages (no parent) and their replies efficiently
    messages = Message.objects.filter(parent_message__isnull=True) \
        .select_related('author') \
        .prefetch_related('replies__author')

    return render(request, 'messaging/threaded_messages.html', {'messages': messages})
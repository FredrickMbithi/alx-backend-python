from django.views.decorators.cache import cache_page
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from messaging.models import Message

@cache_page(60)  # Cache for 60 seconds
@login_required
def message_list(request):
    """Display list of messages with caching"""
    messages = Message.objects.filter(
        receiver=request.user
    ).select_related('sender').order_by('-timestamp')
    
    context = {
        'messages': messages,
    }
    return render(request, 'chats/message_list.html', context)
# chats/filters.py

import django_filters
from django_filters import rest_framework as filters
from django.contrib.auth.models import User
from .models import Message, Conversation

class MessageFilter(filters.FilterSet):
    """
    Filter messages by conversation, sender, content, and date range
    """
    # Filter by conversation ID
    conversation = filters.NumberFilter(field_name='conversation__id')
    
    # Filter by sender username or ID
    sender = filters.NumberFilter(field_name='sender__id')
    sender_username = filters.CharFilter(field_name='sender__username', lookup_expr='icontains')
    
    # Filter by message content
    content = filters.CharFilter(field_name='message_body', lookup_expr='icontains')
    
    # Date range filters
    created_after = filters.DateTimeFilter(field_name='timestamp', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='timestamp', lookup_expr='lte')
    date_range = filters.DateFromToRangeFilter(field_name='timestamp')
    
    # Filter messages from today, this week, etc.
    created_today = filters.BooleanFilter(method='filter_created_today')
    created_this_week = filters.BooleanFilter(method='filter_created_this_week')
    
    class Meta:
        model = Message
        fields = ['conversation', 'sender', 'sender_username', 'content', 
                 'created_after', 'created_before', 'created_today', 'created_this_week']
    
    def filter_created_today(self, queryset, name, value):
        """Filter messages created today"""
        if value:
            from django.utils import timezone
            today = timezone.now().date()
            return queryset.filter(timestamp__date=today)
        return queryset
    
    def filter_created_this_week(self, queryset, name, value):
        """Filter messages created this week"""
        if value:
            from django.utils import timezone
            from datetime import timedelta
            week_ago = timezone.now() - timedelta(days=7)
            return queryset.filter(timestamp__gte=week_ago)
        return queryset

class ConversationFilter(filters.FilterSet):
    """
    Filter conversations by participants and date
    """
    # Filter conversations with specific user
    participant = filters.NumberFilter(method='filter_by_participant')
    participant_username = filters.CharFilter(method='filter_by_participant_username')
    
    # Date range filters
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    
    # Filter by conversation type or other attributes
    has_messages = filters.BooleanFilter(method='filter_has_messages')
    
    class Meta:
        model = Conversation
        fields = ['participant', 'participant_username', 'created_after', 'created_before', 'has_messages']
    
    def filter_by_participant(self, queryset, name, value):
        """Filter conversations where specific user ID is a participant"""
        if value:
            return queryset.filter(participants__id=value)
        return queryset
    
    def filter_by_participant_username(self, queryset, name, value):
        """Filter conversations where user with specific username is a participant"""
        if value:
            return queryset.filter(participants__username__icontains=value)
        return queryset
    
    def filter_has_messages(self, queryset, name, value):
        """Filter conversations that have or don't have messages"""
        if value is True:
            return queryset.filter(messages__isnull=False).distinct()
        elif value is False:
            return queryset.filter(messages__isnull=True)
        return queryset
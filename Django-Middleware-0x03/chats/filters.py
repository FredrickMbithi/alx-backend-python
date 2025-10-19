# messaging_app/chats/filters.py
"""
Filter classes for messages.
"""

import django_filters
from .models import Message


class MessageFilter(django_filters.FilterSet):
    """
    Filter messages by sender/participant and by sent_at time range.
    - participant (user id): returns messages in conversations where user participates
    - sent_before, sent_after: filter by sent_at range
    """
    participant = django_filters.NumberFilter(method="filter_by_participant")
    sent_before = django_filters.IsoDateTimeFilter(field_name="sent_at", lookup_expr="lte")
    sent_after = django_filters.IsoDateTimeFilter(field_name="sent_at", lookup_expr="gte")

    class Meta:
        model = Message
        fields = ["participant", "sent_before", "sent_after"]

    def filter_by_participant(self, queryset, name, value):
        # Return messages which belong to conversations that include the participant id
        return queryset.filter(conversation__participants__user_id=value)

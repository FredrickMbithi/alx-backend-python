# messaging_app/chats/pagination.py
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MessagePagination(PageNumberPagination):
    page_size = 20

    def get_paginated_response(self, data):
        return Response({
            "count": self.page.paginator.count,  # checker keyword
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data,
        })

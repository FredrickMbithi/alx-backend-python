import os
from datetime import datetime
from django.conf import settings
"""
Custom middleware for Django-Middleware-0x03 project.

Implements:
1. RequestLoggingMiddleware  -> Logs user requests with timestamp.
2. RestrictAccessByTimeMiddleware -> Restricts chat access outside allowed hours.
3. OffensiveLanguageMiddleware -> Rate limits messages per IP (max 5/min).
4. RolePermissionMiddleware  -> Allows only admin/moderator to access certain paths.
"""

import logging
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden

# Configure logging for request logs
logging.basicConfig(
    filename="requests.log",
    level=logging.INFO,
    format="%(message)s"
)


class RequestLoggingMiddleware:
    """
    Middleware that logs each request with timestamp, user, and path.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)
        username = user.username if user and user.is_authenticated else "Anonymous"
        log_entry = f"{datetime.now()} - User: {username} - Path: {request.path}"
        logging.info(log_entry)
        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    """
    Middleware that blocks access outside 6AM - 9PM.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()
        start = datetime.strptime("06:00", "%H:%M").time()
        end = datetime.strptime("21:00", "%H:%M").time()

        if not (start <= now <= end):
            return HttpResponseForbidden("Access restricted to working hours (6AM - 9PM).")

        return self.get_response(request)


class OffensiveLanguageMiddleware:
    """
    Middleware that rate-limits messages per IP:
    - Max 5 POST requests per minute per IP.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_cache = {}  # {ip: [timestamps]}

    def __call__(self, request):
        if request.method == "POST" and "/messages" in request.path:
            ip = self._get_ip(request)
            now = datetime.now()

            if ip not in self.ip_cache:
                self.ip_cache[ip] = []

            # Keep only recent requests (last 1 min)
            self.ip_cache[ip] = [
                ts for ts in self.ip_cache[ip] if now - ts < timedelta(minutes=1)
            ]

            if len(self.ip_cache[ip]) >= 5:
                return HttpResponseForbidden("Rate limit exceeded. Max 5 messages per minute.")

            self.ip_cache[ip].append(now)

        return self.get_response(request)

    def _get_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR", "0.0.0.0")


class RolepermissionMiddleware:
    """
    Middleware that enforces role-based access:
    - Only admin or moderator users can access restricted paths.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if "/admin-action" in request.path:
            user = getattr(request, "user", None)
            if not user or not user.is_authenticated:
                return HttpResponseForbidden("Authentication required.")

            # Role check
            role = getattr(user, "role", "guest")
            if role not in ["admin", "moderator"]:
                return HttpResponseForbidden("You do not have permission to perform this action.")

        return self.get_response(request)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.log_file = os.path.join(settings.BASE_DIR, "requests.log")

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_line = f"{datetime.now()} - User: {user} - Path: {request.path}\n"

        # Ensure the file exists and append
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_line)

        response = self.get_response(request)
        return response
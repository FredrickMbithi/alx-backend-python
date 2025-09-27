# chats/middleware.py

import logging
from datetime import datetime
from django.http import HttpResponseForbidden, JsonResponse
from django.utils import timezone
from django.contrib.auth.models import User
import json
from collections import defaultdict
from django.core.cache import cache
import time

# Configure logging for request logging
logging.basicConfig(
    filename='requests.log',
    level=logging.INFO,
    format='%(message)s',
    filemode='a'
)

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    """
    Middleware to log each user's requests to a file
    """
    
    def __init__(self, get_response):
        """
        Initialize the middleware
        """
        self.get_response = get_response
    
    def __call__(self, request):
        """
        Process the request and log user activity
        """
        # Get user info
        if request.user.is_authenticated:
            user = request.user.username
        else:
            user = "Anonymous"
        
        # Create log entry
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        
        # Log to file
        logger.info(log_message)
        
        # Also log to console for development
        print(log_message)
        
        # Continue processing the request
        response = self.get_response(request)
        
        return response


class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict chat access during certain hours
    Only allows access between 6 AM and 9 PM
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Check if this is a chat-related request
        if request.path.startswith('/api/chats/'):
            current_hour = timezone.now().hour
            
            # Block access outside 6 AM (6) to 9 PM (21) hours
            if current_hour < 6 or current_hour >= 21:
                return JsonResponse({
                    'error': 'Chat access is restricted during these hours. Available from 6 AM to 9 PM.',
                    'current_time': timezone.now().strftime('%H:%M:%S'),
                    'status': 'forbidden'
                }, status=403)
        
        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware:
    """
    Middleware to implement rate limiting based on IP address
    Limits users to 5 messages per minute
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Store message counts per IP with timestamps
        self.message_counts = defaultdict(list)
        self.rate_limit = 5  # messages per minute
        self.time_window = 60  # seconds
    
    def __call__(self, request):
        # Only apply to POST requests on message endpoints
        if (request.method == 'POST' and 
            request.path.startswith('/api/chats/messages')):
            
            # Get client IP address
            ip_address = self.get_client_ip(request)
            current_time = time.time()
            
            # Clean old entries (older than time window)
            self.message_counts[ip_address] = [
                timestamp for timestamp in self.message_counts[ip_address]
                if current_time - timestamp < self.time_window
            ]
            
            # Check if user has exceeded rate limit
            if len(self.message_counts[ip_address]) >= self.rate_limit:
                return JsonResponse({
                    'error': f'Rate limit exceeded. Maximum {self.rate_limit} messages per minute.',
                    'retry_after': '60 seconds',
                    'current_count': len(self.message_counts[ip_address])
                }, status=429)
            
            # Add current timestamp
            self.message_counts[ip_address].append(current_time)
        
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        """
        Get the client's IP address from the request
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RolepermissionMiddleware:
    """
    Middleware to check user roles before allowing access to specific actions
    Only allows admin and moderator users to access certain endpoints
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Define protected paths that require admin/moderator access
        self.protected_paths = [
            '/api/chats/conversations/',  # Creating conversations
            '/admin/',  # Admin panel
        ]
        # Define roles that have access
        self.allowed_roles = ['admin', 'moderator']
    
    def __call__(self, request):
        # Check if the path requires role-based permission
        if self.requires_role_permission(request.path):
            # Check if user is authenticated
            if not request.user.is_authenticated:
                return JsonResponse({
                    'error': 'Authentication required',
                    'status': 'unauthorized'
                }, status=401)
            
            # Check if user has required role
            if not self.user_has_required_role(request.user):
                return JsonResponse({
                    'error': 'Access denied. Admin or moderator role required.',
                    'user_role': self.get_user_role(request.user),
                    'required_roles': self.allowed_roles
                }, status=403)
        
        response = self.get_response(request)
        return response
    
    def requires_role_permission(self, path):
        """
        Check if the path requires role-based permissions
        """
        # For POST requests to create conversations or access admin
        return any(path.startswith(protected_path) for protected_path in self.protected_paths)
    
    def user_has_required_role(self, user):
        """
        Check if user has admin or moderator role
        """
        # Check if user is superuser (admin)
        if user.is_superuser or user.is_staff:
            return True
        
        # Check if user has admin or moderator group
        user_groups = user.groups.values_list('name', as_list=True)
        return any(role in user_groups for role in self.allowed_roles)
    
    def get_user_role(self, user):
        """
        Get the user's role for debugging purposes
        """
        if user.is_superuser:
            return 'superuser'
        elif user.is_staff:
            return 'staff'
        else:
            user_groups = list(user.groups.values_list('name', flat=True))
            return user_groups[0] if user_groups else 'regular_user'
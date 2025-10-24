from django.http import JsonResponse

class RolepermissionMiddleware:
    """
    Middleware to check user roles before allowing access to specific actions.
    Only allows admin and moderator users to access certain endpoints.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Protected paths that require admin/moderator access
        self.protected_paths = [
            "/api/chats/conversations/",  # Creating conversations
            "/admin/",                    # Admin panel
        ]
        # Roles that are allowed
        self.allowed_roles = ["admin", "moderator"]

    def __call__(self, request):
        # Check if this path requires role-based permission
        if self.requires_role_permission(request.path):
            # User must be authenticated
            if not request.user.is_authenticated:
                return JsonResponse(
                    {"error": "Authentication required", "status": "unauthorized"},
                    status=401
                )

            # User must have correct role
            if not self.user_has_required_role(request.user):
                return JsonResponse(
                    {
                        "error": "Access denied. Admin or moderator role required.",
                        "user_role": self.get_user_role(request.user),
                        "required_roles": self.allowed_roles,
                    },
                    status=403
                )

        # Continue normal processing
        response = self.get_response(request)
        return response

    def requires_role_permission(self, path):
        """Check if the path requires role-based permissions"""
        return any(path.startswith(protected) for protected in self.protected_paths)

    def user_has_required_role(self, user):
        """Check if user has admin or moderator role"""
        # Superuser/staff always allowed
        if user.is_superuser or user.is_staff:
            return True
        # Check user groups
        user_groups = user.groups.values_list("name", flat=True)
        return any(role in user_groups for role in self.allowed_roles)

    def get_user_role(self, user):
        """Get the user's role for debugging purposes"""
        if user.is_superuser:
            return "superuser"
        elif user.is_staff:
            return "staff"
        else:
            user_groups = list(user.groups.values_list("name", flat=True))
            return user_groups[0] if user_groups else "regular_user"

from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """Custom permission class to allow only alumnos to view and edit them."""

    def has_object_permission(self, request, view, obj):
        """Return True if permission is granted to the alumno user."""
        return False
        return obj.owner == request.user

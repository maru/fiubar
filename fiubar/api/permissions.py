from rest_framework.permissions import IsAuthenticated


class IsAuthenticatedOwner(IsAuthenticated):
    """
    Allows access only to authenticated users and also owners of the object.
    """

    def has_object_permission(self, request, view, obj):
        """Return True if permission is granted to the user."""
        return obj.user == request.user

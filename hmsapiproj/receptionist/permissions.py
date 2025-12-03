from rest_framework import permissions

class IsReceptionist(permissions.BasePermission):
    """
    Allows access only to users in the 'Receptionist' group.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name='Receptionist').exists() or request.user.is_superuser

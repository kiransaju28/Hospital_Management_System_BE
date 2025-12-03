from rest_framework import permissions

class IsLabTech(permissions.BasePermission):
    """
    Allows access only to users in the 'LabTech' group.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name='LabTech').exists() or request.user.is_superuser


from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Allows access to users in the 'Admin' group OR superusers.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.groups.filter(name='Admin').exists()
            )
        )


class IsDoctor(permissions.BasePermission):
    """
    Allows access only to users in the 'Doctor' group.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name='Doctor').exists()
        )


class Islabtech(permissions.BasePermission):
    """
    Allows access only to users in the 'labtech' group.
    (Group name must be exactly 'labtech')
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name='labtech').exists()
        )


class IsReceptionist(permissions.BasePermission):
    """
    Allows access only to users in the 'receptionist' group.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name='receptionist').exists()
        )


class IsPharmacist(permissions.BasePermission):
    """
    Allows access only to users in the 'Pharmacist' group.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name='Pharmacist').exists()
        )

# doctor/permissions.py

from rest_framework import permissions


class IsDoctorUser(permissions.BasePermission):
    """
    Allows access only to authenticated users in the 'Doctor' group.
    (Currently you are using admins.permissions.IsDoctor,
    but this is here if you want a doctor-local permission.)
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name='Doctor').exists()
        )

from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Staff, Doctor, Specialization
from .serializers import (
    StaffSerializer,
    DoctorSerializer,
    SpecializationSerializer,
    UserRegistrationSerializer,
)

from .permissions import IsAdmin


class RegisterUserViewSet(viewsets.ModelViewSet):
    """
    Used by admin to create users (Doctor, LabTech, Receptionist, Pharmacist, etc.)
    """
    queryset = Staff.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class StaffViewSet(viewsets.ModelViewSet):
    """
    View all staff (for admins).
    Supports Create, Read, Update, Delete.
    Deleting a staff member will also delete the associated User account.
    """
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [AllowAny]

    def perform_destroy(self, instance):
        # Delete the associated User. 
        # Since Staff has on_delete=CASCADE on the user field, 
        # deleting the User might delete the Staff, or we just delete the User.
        # However, usually we want to remove the login access too.
        user = instance.user
        if user:
            user.delete()
        else:
            instance.delete()


class DoctorViewSet(viewsets.ModelViewSet):
    """
    View all doctors (for admins).
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [AllowAny]


class SpecializationViewSet(viewsets.ModelViewSet):
    """
    CRUD for doctor specializations.
    """
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    permission_classes = [AllowAny]

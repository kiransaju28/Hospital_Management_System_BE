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


class StaffViewSet(viewsets.ReadOnlyModelViewSet):
    """
    View all staff (for admins).
    """
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [IsAdmin]


class DoctorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    View all doctors (for admins).
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAdmin]


class SpecializationViewSet(viewsets.ModelViewSet):
    """
    CRUD for doctor specializations.
    """
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    permission_classes = [IsAdmin]

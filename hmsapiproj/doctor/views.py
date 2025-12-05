from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from admins.permissions import IsDoctor
from .models import (
    BasicVitals,
    Consultation,
    PrescriptionItem,
    LabTestOrder,
)
from .serializers import (
    BasicVitalsSerializer,
    ConsultationSerializer,
    PrescriptionItemSerializer,
    LabTestOrderSerializer,
)

from receptionist.models import Appointment, Patient         # FIXED
from receptionist.serializers import AppointmentSerializer   # FIXED


# --------------------------
# TODAY'S APPOINTMENTS
# --------------------------
class TodayAppointmentsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        from django.utils.timezone import now
        today = now().date()
        return Appointment.objects.filter(appointment_date__date=today)


# --------------------------
# BASIC VITALS
# --------------------------
class BasicVitalsViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = BasicVitals.objects.all()
    serializer_class = BasicVitalsSerializer


# --------------------------
# CONSULTATION
# --------------------------
class ConsultationViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer


# --------------------------
# PRESCRIPTION
# --------------------------
class PrescriptionItemViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = PrescriptionItem.objects.all()
    serializer_class = PrescriptionItemSerializer


# --------------------------
# LAB TEST ORDER
# --------------------------
class LabTestOrderViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = LabTestOrder.objects.all()
    serializer_class = LabTestOrderSerializer

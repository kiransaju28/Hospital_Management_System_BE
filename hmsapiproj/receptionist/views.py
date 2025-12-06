from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from .models import Patient, Appointment, ConsultationBill
from .serializers import (
    PatientSerializer,
    AppointmentSerializer,
    ConsultationBillSerializer,
)

from admins.permissions import IsReceptionist


class PatientViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Patient.objects.all().order_by("Patient_id")
    serializer_class = PatientSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ["patient_name", "phone"]


class AppointmentViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Appointment.objects.all().order_by("Appointment_id")
    serializer_class = AppointmentSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ["token", "patient__patient_name"]


class ConsultationBillViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = ConsultationBill.objects.all().order_by("ConsultationBill_id")
    serializer_class = ConsultationBillSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ["patient__patient_name", "appointment__token"]

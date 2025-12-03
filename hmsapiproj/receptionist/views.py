from rest_framework import viewsets, filters
from .models import Patient, Appointment, ConsultationBill
from .serializers import (
    PatientSerializer,
    AppointmentSerializer,
    ConsultationBillSerializer,
)

from admins.permissions import Isreceptionist


class PatientViewSet(viewsets.ModelViewSet):
    permission_classes = [Isreceptionist]
    queryset = Patient.objects.all().order_by("Patient_id")
    serializer_class = PatientSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ["patient_name", "phone"]


class AppointmentViewSet(viewsets.ModelViewSet):
    permission_classes = [Isreceptionist]
    queryset = Appointment.objects.all().order_by("Appointment_id")
    serializer_class = AppointmentSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ["token", "patient__patient_name"]


class ConsultationBillViewSet(viewsets.ModelViewSet):
    permission_classes = [Isreceptionist]
    queryset = ConsultationBill.objects.all().order_by("ConsultationBill_id")
    serializer_class = ConsultationBillSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ["patient__patient_name", "appointment__token"]

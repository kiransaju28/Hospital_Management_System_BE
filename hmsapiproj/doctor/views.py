from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from admins.permissions import IsAdmin, IsDoctor,Islabtech
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
    permission_classes = [IsDoctor | IsAdmin]
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        from django.utils.timezone import now
        today = now().date()
        return Appointment.objects.filter(
            appointment_date__date=today,
            doctor__staff__user=self.request.user
        )


# --------------------------
# BASIC VITALS
# --------------------------
class BasicVitalsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsDoctor | IsAdmin]
    queryset = BasicVitals.objects.all()
    serializer_class = BasicVitalsSerializer


# --------------------------
# CONSULTATION
# --------------------------
class ConsultationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsDoctor | IsAdmin]
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer


# --------------------------
# PRESCRIPTION
# --------------------------
class PrescriptionItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsDoctor | IsAdmin]
    queryset = PrescriptionItem.objects.all()
    serializer_class = PrescriptionItemSerializer


# --------------------------
# LAB TEST ORDER
# --------------------------
class LabTestOrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsDoctor | IsAdmin |Islabtech]
    queryset = LabTestOrder.objects.all()
    serializer_class = LabTestOrderSerializer


# --------------------------
# EXTERNAL DATA (READ-ONLY)
# --------------------------
from pharmacist.models import Medicine
from pharmacist.serializers import MedicineSerializer
from labtech.models import LabTestCategory
from labtech.serializers import LabTestCategorySerializer

class PharmacistMedicineViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsDoctor | IsAdmin|Islabtech]
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer

class LabTestCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsDoctor | IsAdmin|Islabtech]
    queryset = LabTestCategory.objects.all()
    serializer_class = LabTestCategorySerializer

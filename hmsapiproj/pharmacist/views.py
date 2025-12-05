from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from admins.permissions import IsPharmacist
from .models import Medicine, pharmacistBill
from .serializers import MedicineSerializer, pharmacistBillSerializer

# --- Import Doctor models for the workflow ---
from doctor.models import Consultation
from doctor.serializers import ConsultationSerializer


class MedicineViewSet(viewsets.ModelViewSet):
    """
    Manage Inventory (Add/Edit/Delete medicines).
    Only Pharmacists can do this.
    """
    permission_classes = [AllowAny]
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['medicine_name']


class PendingPrescriptionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    WORKFLOW: Shows consultations where the doctor ordered medicines
    ('fulfill_pharmacist_internally'=True) but they haven't been billed yet.
    This is the Pharmacist's "To-Do List".
    """
    permission_classes = [AllowAny]
    serializer_class = ConsultationSerializer  # Re-use the doctor's serializer to see the meds

    def get_queryset(self):
        # 1. Doctor said "Internal pharmacist"
        # 2. Has prescription items
        # 3. NOT in pharmacistBill table yet (simplified check)

        # Get IDs of consultations that are already billed
        billed_ids = pharmacistBill.objects.values_list('consultation_id', flat=True)

        return Consultation.objects.filter(
            fulfill_pharmacist_internally=True,
            prescription_items__isnull=False
        ).exclude(id__in=billed_ids).distinct().order_by('Consultation_id')


class pharmacistBillViewSet(viewsets.ModelViewSet):
    """
    Generate Bills.
    When a bill is created, it automatically subtracts stock (via Serializer).
    """
    permission_classes = [AllowAny]
    queryset = pharmacistBill.objects.all().order_by('pharmacistBill_id')
    serializer_class = pharmacistBillSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['patient__patient_name']

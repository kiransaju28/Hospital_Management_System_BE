from rest_framework import serializers

from .models import (
    BasicVitals,
    Consultation,
    PrescriptionItem,
    LabTestOrder,
)

from receptionist.models import Appointment, Patient      # FIXED
from pharmacist.models import Medicine
from labtech.models import LabTestCategory


# --------------------------
# VITALS
# --------------------------
class BasicVitalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicVitals
        fields = "__all__"


# --------------------------
# CONSULTATION
# --------------------------
class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = "__all__"


# --------------------------
# PRESCRIPTION
# --------------------------
class PrescriptionItemSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source="medicine.medicine_name", read_only=True)

    class Meta:
        model = PrescriptionItem
        fields = "__all__"


# --------------------------
# LAB TEST ORDER
# --------------------------
class LabTestOrderSerializer(serializers.ModelSerializer):
    test_name = serializers.CharField(source="test.category_name", read_only=True)

    class Meta:
        model = LabTestOrder
        fields = "__all__"

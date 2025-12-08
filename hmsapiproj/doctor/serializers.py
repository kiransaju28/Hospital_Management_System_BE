from rest_framework import serializers
from .models import (
    BasicVitals,
    Consultation,
    PrescriptionItem,
    LabTestOrder,
)

# --------------------------
# VITALS
# --------------------------
class BasicVitalsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)
    class Meta:
        model = BasicVitals
        fields = "__all__"

# --------------------------
# CONSULTATION
# --------------------------
class ConsultationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)
    patient_name = serializers.CharField(source='appointment.patient.patient_name', read_only=True)
    class Meta:
        model = Consultation
        fields = "__all__"

# --------------------------
# PRESCRIPTION
# --------------------------
class PrescriptionItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)
    medicine_name = serializers.CharField(source="medicine.medicine_name", read_only=True)
    class Meta:
        model = PrescriptionItem
        fields = "__all__"

# --------------------------
# LAB TEST ORDER
# --------------------------
class LabTestOrderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)
    test_name = serializers.CharField(source="test.category_name", read_only=True)
    patient_name = serializers.CharField(
        source="consultation.appointment.patient.patient_name", 
        read_only=True
    )
    report_id = serializers.SerializerMethodField()

    class Meta:
        model = LabTestOrder
        fields = "__all__"

    def get_report_id(self, obj):
        # Use reverse relationship from LabReport (foreign key to LabTestOrder)
        # Verify if related_name is default 'labreport_set'
        report = obj.labreport_set.first()
        return report.LabReport_id if report else None

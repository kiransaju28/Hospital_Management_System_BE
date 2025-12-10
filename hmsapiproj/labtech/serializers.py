from rest_framework import serializers
from .models import (
    LabTestCategory,
    LabTestParameter,
    LabReport,
    LabReportResult,
    LabBill,
    LabBillItem,
)

from .validations import (
    validate_lab_report_fields,
    validate_lab_result_value,
)


# --------------------------
# CATEGORY & PARAMETERS
# --------------------------

class LabTestCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTestCategory
        fields = "__all__"


class LabTestParameterSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.category_name", read_only=True)

    class Meta:
        model = LabTestParameter
        fields = [
            "LabTestParameter_id",
            "category",
            "category_name",
            "label",
            "normal_range",
        ]


# --------------------------
# LAB REPORT
# --------------------------

class LabReportResultSerializer(serializers.ModelSerializer):
    parameter_name = serializers.CharField(source="parameter.label", read_only=True)
    normal_range = serializers.CharField(source="parameter.normal_range", read_only=True)

    class Meta:
        model = LabReportResult
        fields = "__all__"

    def validate(self, data):
        return validate_lab_result_value(data)


class LabReportSerializer(serializers.ModelSerializer):
    results = LabReportResultSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source="category.category_name", read_only=True)
    patient_name = serializers.CharField(
        source="order.consultation.appointment.patient.patient_name", 
        read_only=True
    )
    patient_id = serializers.IntegerField(
        source="order.consultation.appointment.patient.Patient_id",
        read_only=True
    )

    class Meta:
        model = LabReport
        fields = "__all__"

    def validate(self, data):
        return validate_lab_report_fields(data)


# --------------------------
# LAB BILL
# --------------------------

class LabBillItemSerializer(serializers.ModelSerializer):
    test_name = serializers.CharField(source="test.category_name", read_only=True)

    class Meta:
        model = LabBillItem
        fields = "__all__"


class LabBillSerializer(serializers.ModelSerializer):
    items = LabBillItemSerializer(many=True)
    patient_name = serializers.CharField(source="patient.patient_name", read_only=True)

    class Meta:
        model = LabBill
        fields = "__all__"
        read_only_fields = ["bill_date", "total_amount"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        bill = LabBill.objects.create(total_amount=0, **validated_data)

        total = 0
        for item in items_data:
            test = item["test"]
            price = item["price"]
            subtotal = price

            LabBillItem.objects.create(
                bill=bill,
                test=test,
                price=price,
                subtotal=subtotal,
            )

            total += subtotal

        bill.total_amount = total
        bill.save()
        return bill

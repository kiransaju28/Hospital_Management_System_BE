from rest_framework import serializers
from django.contrib.auth.models import User, Group

from .models import Staff, Doctor, Specialization
from receptionist.models import ConsultationBill, Patient
from labtech.models import LabBill
from pharmacist.models import pharmacistBill

from .validations import (
    validate_unique_username,
    validate_mobile_number,
    validate_gender,
    validate_role,
    validate_doctor_required_fields,
)


# ==========================================================
# USER REGISTRATION
# ==========================================================
class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    role = serializers.CharField()

    full_name = serializers.CharField()
    gender = serializers.CharField()
    joining_date = serializers.DateField()
    mobile_number = serializers.CharField()

    consultation_fee = serializers.IntegerField(required=False)
    designation = serializers.CharField(required=False, allow_blank=True)
    availability = serializers.CharField(required=False, allow_blank=True)
    specialization = serializers.PrimaryKeyRelatedField(
        queryset=Specialization.objects.all(),
        required=False,
    )

    def validate_username(self, value):
        return validate_unique_username(value)

    def validate_mobile_number(self, value):
        return validate_mobile_number(value)

    def validate_gender(self, value):
        return validate_gender(value)

    def validate_role(self, value):
        return validate_role(value)

    def validate(self, data):
        if data.get("role") == "Doctor":
            validate_doctor_required_fields(data)
        return data

    def create(self, validated_data):
        role_name = validated_data["role"]

        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )

        group, _ = Group.objects.get_or_create(name=role_name)
        user.groups.add(group)

        staff = Staff.objects.create(
            user=user,
            full_name=validated_data["full_name"],
            gender=validated_data["gender"],
            joining_date=validated_data["joining_date"],
            mobile_number=validated_data["mobile_number"],
        )

        if role_name == "Doctor":
            Doctor.objects.create(
                staff=staff,
                consultation_fee=validated_data["consultation_fee"],
                designation=validated_data.get("designation", ""),
                specialization=validated_data["specialization"],
                availability=validated_data.get("availability", ""),
            )

        return user


# ==========================================================
# SPECIALIZATION
# ==========================================================
class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ["spec_Id", "specialization_name"]


# ==========================================================
# STAFF
# ==========================================================
class StaffSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    role = serializers.CharField(source="user.groups.first.name", read_only=True)

    class Meta:
        model = Staff
        fields = [
            "staff_id",
            "full_name",
            "gender",
            "joining_date",
            "mobile_number",
            "username",
            "role",
        ]


# ==========================================================
# DOCTOR
# ==========================================================
class DoctorSerializer(serializers.ModelSerializer):
    staff = StaffSerializer(read_only=True)

    class Meta:
        model = Doctor
        fields = [
            "doctor_id",
            "staff",
            "consultation_fee",
            "designation",
            "availability",
            "specialization",
        ]


# ==========================================================
# BILL SUMMARIES (for possible admin dashboards)
# ==========================================================
class SimpleConsultationBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationBill
        fields = ["bill_date", "amount"]


class SimpleLabBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabBill
        fields = ["bill_date", "total_amount"]


class SimplePharmacyBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = pharmacistBill
        fields = ["bill_date", "total_amount"]

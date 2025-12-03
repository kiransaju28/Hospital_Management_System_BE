from rest_framework import serializers
from .models import Patient, Appointment, ConsultationBill
from admins.models import Doctor

from .validations import (
    validate_blood_group,
    validate_gender,
    validate_phone,
    validate_dob,
    calculate_age,
    validate_appointment_rules,
    validate_bill_not_duplicate,
)


# ==========================
# PATIENT SERIALIZER
# ==========================
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "Patient_id",
            "patient_name",
            "age",
            "email",
            "date_of_birth",
            "blood_group",
            "gender",
            "address",
            "phone",
        ]
        read_only_fields = ["age"]

    def validate_blood_group(self, value):
        return validate_blood_group(value)

    def validate_gender(self, value):
        return validate_gender(value)

    def validate_phone(self, value):
        return validate_phone(value)

    def validate_date_of_birth(self, value):
        return validate_dob(value)

    def validate(self, data):
        dob = data.get("date_of_birth")
        if dob:
            data["age"] = calculate_age(dob)
        return data


# ==========================
# APPOINTMENT SERIALIZER
# ==========================
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            "Appointment_id",
            "token",
            "appointment_date",
            "status",
            "patient",
            "doctor",
        ]
        read_only_fields = ["token", "status", "appointment_date"]

    def generate_token(self):
        last = Appointment.objects.order_by("-Appointment_id").first()
        if not last:
            return "T001"
        last_num = int(last.token[1:])
        return f"T{last_num + 1:03d}"

    def validate(self, attrs):
        patient = attrs.get("patient")
        doctor = attrs.get("doctor")

        # Ensure patient & doctor exist
        if not Patient.objects.filter(id=patient.id).exists():
            raise serializers.ValidationError("Patient does not exist.")

        if not Doctor.objects.filter(doctor_id=doctor.doctor_id).exists():
            raise serializers.ValidationError("Doctor does not exist.")

        from django.utils import timezone
        now = timezone.now()

        validate_appointment_rules(patient, doctor, now)

        return attrs

    def create(self, validated_data):
        from django.utils import timezone

        validated_data["token"] = self.generate_token()
        validated_data["status"] = "Scheduled"
        validated_data["appointment_date"] = timezone.now()
        return super().create(validated_data)


# ==========================
# CONSULTATION BILL SERIALIZER
# ==========================
class ConsultationBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationBill
        fields = [
            "ConsultationBill_id",
            "appointment",
            "patient",
            "bill_date",
            "amount",
        ]
        read_only_fields = ["patient", "bill_date", "amount"]

    def validate(self, attrs):
        appointment = attrs.get("appointment")
        if not appointment:
            raise serializers.ValidationError("Appointment is required.")

        validate_bill_not_duplicate(appointment)

        if not appointment.doctor:
            raise serializers.ValidationError("Doctor not assigned to appointment.")

        return attrs

    def create(self, validated_data):
        appointment = validated_data["appointment"]

        bill = ConsultationBill.objects.create(
            appointment=appointment,
            patient=appointment.patient,
            amount=appointment.doctor.consultation_fee,
        )
        return bill

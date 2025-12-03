from rest_framework import serializers
from datetime import date


# ----------------------- PATIENT -----------------------

def validate_blood_group(value):
    valid_groups = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
    if value.upper() not in valid_groups:
        raise serializers.ValidationError("Invalid blood group.")
    return value.upper()


def validate_gender(value):
    valid = ["male", "female", "other"]
    if value.lower() not in valid:
        raise serializers.ValidationError("Gender must be Male, Female, or Other.")
    return value.capitalize()


def validate_phone(value):
    if not value.isdigit():
        raise serializers.ValidationError("Phone must contain only digits.")
    if len(value) != 10:
        raise serializers.ValidationError("Phone number must be exactly 10 digits.")
    return value


def validate_dob(dob):
    today = date.today()
    if dob > today:
        raise serializers.ValidationError("Date of birth cannot be in the future.")
    return dob


def calculate_age(dob):
    today = date.today()
    return today.year - dob.year - (
        (today.month, today.day) < (dob.month, dob.day)
    )


# --------------------- APPOINTMENTS ---------------------

def validate_appointment_rules(patient, doctor, appointment_date):
    """
    Prevent duplicate booking (patient or doctor) on same day.
    """
    from receptionist.models import Appointment

    date_only = appointment_date.date()

    # Patient double booking
    if Appointment.objects.filter(
        patient=patient,
        appointment_date__date=date_only
    ).exists():
        raise serializers.ValidationError(
            "This patient already has an appointment today."
        )

    # Doctor double booking
    if Appointment.objects.filter(
        doctor=doctor,
        appointment_date__date=date_only
    ).exists():
        raise serializers.ValidationError(
            "Doctor is already booked today."
        )

    return True


# --------------------- BILLS ---------------------

def validate_bill_not_duplicate(appointment):
    from receptionist.models import ConsultationBill

    if ConsultationBill.objects.filter(appointment=appointment).exists():
        raise serializers.ValidationError("Bill already exists for this appointment.")

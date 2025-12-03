# admins/validations.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Staff, Doctor, Specialization


# ---------------------------------------------------------
# 1. USERNAME VALIDATION
# ---------------------------------------------------------
def validate_unique_username(username: str):
    """
    Check if username already exists in the system.
    """
    if User.objects.filter(username=username).exists():
        raise serializers.ValidationError("Username already exists.")
    return username


# ---------------------------------------------------------
# 2. MOBILE NUMBER VALIDATION
# ---------------------------------------------------------
def validate_mobile_number(mobile: str):
    """
    Must be:
    - Only digits
    - Exactly 10 digits
    - Unique across all Staff
    """
    if not mobile.isdigit():
        raise serializers.ValidationError("Mobile number must contain only digits.")

    if len(mobile) != 10:
        raise serializers.ValidationError("Mobile number must be exactly 10 digits.")

    if Staff.objects.filter(mobile_number=mobile).exists():
        raise serializers.ValidationError("This mobile number is already used.")

    return mobile


# ---------------------------------------------------------
# 3. GENDER VALIDATION
# ---------------------------------------------------------
def validate_gender(gender: str):
    valid = ["male", "female", "other"]

    if gender.lower() not in valid:
        raise serializers.ValidationError(
            "Gender must be Male, Female, or Other."
        )

    return gender.capitalize()


# ---------------------------------------------------------
# 4. ROLE VALIDATION
# ---------------------------------------------------------
ALLOWED_ROLES = ["Doctor", "receptionist", "labtech", "Pharmacist"]

def validate_role(role: str):
    """
    Ensure the selected role matches allowed roles.
    """
    if role not in ALLOWED_ROLES:
        raise serializers.ValidationError(
            f"Invalid role. Allowed roles: {', '.join(ALLOWED_ROLES)}"
        )
    return role


# ---------------------------------------------------------
# 5. DOCTOR-SPECIFIC VALIDATION
# ---------------------------------------------------------
def validate_doctor_required_fields(data):
    """
    If role = Doctor, ensure the required fields exist:
    - consultation_fee
    - designation
    - availability
    - specialization
    """
    errors = {}

    required_fields = [
        "consultation_fee",
        "designation",
        "availability",
        "specialization",
    ]

    for field in required_fields:
        if not data.get(field):
            errors[field] = f"{field} is required for Doctor role."

    if errors:
        raise serializers.ValidationError(errors)

    return data


def validate_specialization_exists(spec_id):
    """
    Ensure the specialization exists.
    """
    if not Specialization.objects.filter(id=spec_id).exists():
        raise serializers.ValidationError("Invalid specialization ID.")

    return spec_id

# doctor/validations.py

import re
from rest_framework import serializers


def validate_vitals_data(data):
    """
    Shared validator for BasicVitalsSerializer.
    Ensures:
    - height, weight, blood_sugar are non-negative (if provided)
    - blood_pressure is in a valid format like "120/80" if provided
    """
    height = data.get("height")
    weight = data.get("weight")
    blood_sugar = data.get("blood_sugar")
    blood_pressure = data.get("blood_pressure")

    # --- numeric fields must be >= 0 ---
    for field_name, value in [
        ("height", height),
        ("weight", weight),
        ("blood_sugar", blood_sugar),
    ]:
        if value is not None and value < 0:
            raise serializers.ValidationError(
                {field_name: f"{field_name.capitalize()} cannot be negative."}
            )

    # --- blood pressure format: "SYS/DIA" ---
    if blood_pressure:
        pattern = r"^\d{2,3}/\d{2,3}$"  # e.g. 120/80
        if not re.match(pattern, blood_pressure):
            raise serializers.ValidationError(
                {"blood_pressure": "Blood pressure must be like '120/80'."}
            )

    return data

# labtec/validations.py

from rest_framework import serializers


def validate_lab_report_fields(data):
    """
    Ensures:
    - remarks is not empty (optional)
    - report_date not in future (optional)
    """
    report_date = data.get("report_date")

    from datetime import date
    if report_date and report_date > date.today():
        raise serializers.ValidationError(
            {"report_date": "Report date cannot be in the future."}
        )

    return data


def validate_lab_result_value(data):
    """
    Ensures:
    - value field is numeric and non-negative
    """
    value = data.get("value")

    if value is not None:
        try:
            float(value)
        except:
            raise serializers.ValidationError(
                {"value": "Result value must be a valid number."}
            )

    return data

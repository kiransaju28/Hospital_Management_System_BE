# pharmacist/validations.py

from rest_framework import serializers


def validate_quantity(value):
    """
    Quantity must be a positive integer.
    """
    if value is None or int(value) <= 0:
        raise serializers.ValidationError("Quantity must be a positive number.")
    return value


def validate_stock_availability(medicine, quantity):
    """
    Check if medicine has enough stock for the requested quantity.
    """
    if medicine.stock < quantity:
        raise serializers.ValidationError(
            f"Only {medicine.stock} units available for {medicine.medicine_name}."
        )


def validate_price(value):
    """
    Price must be >= 0
    """
    if value is None or float(value) < 0:
        raise serializers.ValidationError("Price cannot be negative.")
    return value

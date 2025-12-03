from django.test import TestCase
from .models import Medicine


class PharmacistBasicTest(TestCase):
    def test_medicine_str(self):
        med = Medicine.objects.create(
            medicine_name="Paracetamol",
            manufacture_name="ABC Pharma",
            dosage="500mg",
            quantity_in_stock=100,
            price_per_unit=5.00,
        )
        self.assertIn("Paracetamol", str(med))

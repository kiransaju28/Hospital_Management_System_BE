from django.test import TestCase
from .models import Patient


class ReceptionistBasicTest(TestCase):
    def test_patient_creation(self):
        p = Patient.objects.create(
            patient_name="John Doe",
            age=30,
            email="test@example.com",
            date_of_birth="1995-02-01",
            blood_group="A+",
            gender="Male",
            address="Test address",
            phone="9999999999",
        )
        self.assertEqual(str(p), f"{p.patient_name} (ID: {p.Patient_id})")

# doctor/tests.py

from django.test import TestCase
from django.contrib.auth.models import User, Group
from admins.models import Staff, Doctor, Specialization


class SimpleDoctorModelTests(TestCase):
    def test_doctor_can_be_created_with_staff_and_specialization(self):
        user = User.objects.create_user(username="docuser", password="pwd123")
        group, _ = Group.objects.get_or_create(name='Doctor')
        user.groups.add(group)

        staff = Staff.objects.create(
            user=user,
            full_name="Dr Test",
            gender="Male",
            joining_date="2025-01-01",
            mobile_number="9998887776",
        )

        spec = Specialization.objects.create(specialization_name="Cardiology")

        doctor = Doctor.objects.create(
            staff=staff,
            consultation_fee=500,
            designation="Consultant",
            availability="Mon-Fri",
            specialization=spec,
        )

        self.assertEqual(str(doctor), f"Dr. {staff.full_name}")
        self.assertTrue(user.groups.filter(name='Doctor').exists())

from django.test import TestCase
from .models import LabTestCategory

class LabtechSimpleTest(TestCase):
    def test_category_creation(self):
        c = LabTestCategory.objects.create(category_name="Blood Test")
        self.assertEqual(str(c), "Blood Test")

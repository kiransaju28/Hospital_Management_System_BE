from django.test import TestCase


class AdminsSmokeTest(TestCase):
    """
    Simple smoke test to ensure the admins app is correctly installed
    and migrations run without import errors.
    """
    def test_smoke(self):
        self.assertTrue(True)

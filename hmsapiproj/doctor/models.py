from django.db import models


class BasicVitals(models.Model):
    vitals_id = models.AutoField(primary_key=True)

    appointment = models.OneToOneField(
        "receptionist.Appointment",
        on_delete=models.CASCADE
    )

    height = models.FloatField()
    weight = models.FloatField()
    blood_pressure = models.CharField(max_length=20)
    blood_sugar = models.FloatField()

    def __str__(self):
        return f"Vitals {self.vitals_id}"


class Consultation(models.Model):
    consultation_id = models.AutoField(primary_key=True)

    appointment = models.OneToOneField(
        "receptionist.Appointment",
        on_delete=models.CASCADE
    )

    vitals = models.OneToOneField(
        BasicVitals,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    symptoms = models.TextField()
    diagnosis = models.TextField()
    notes = models.TextField()

    fulfill_pharmacist_internally = models.BooleanField(default=False)

    def __str__(self):
        return f"Consultation {self.consultation_id}"


class PrescriptionItem(models.Model):
    prescription_item_id = models.AutoField(primary_key=True)

    consultation = models.ForeignKey(
        Consultation,
        on_delete=models.CASCADE,
        related_name="prescription_items"
    )

    medicine = models.ForeignKey(
        "pharmacist.Medicine",
        on_delete=models.PROTECT
    )

    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)

    def __str__(self):
        return f"Prescription {self.prescription_item_id}"


class LabTestOrder(models.Model):
    lab_test_order_id = models.AutoField(primary_key=True)

    consultation = models.ForeignKey(
        Consultation,
        on_delete=models.CASCADE
    )

    test = models.ForeignKey(
        "labtech.LabTestCategory",
        on_delete=models.PROTECT
    )

    status = models.CharField(max_length=20, default="Pending")

    def __str__(self):
        return f"Lab Test Order {self.lab_test_order_id}"

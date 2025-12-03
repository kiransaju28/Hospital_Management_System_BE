from django.db import models


from django.db import models


class Patient(models.Model):
    Patient_id = models.AutoField(primary_key=True)
    patient_name = models.CharField(max_length=40)
    age = models.IntegerField()
    email = models.EmailField(max_length=40, unique=True, null=True, blank=True)
    date_of_birth = models.DateField()
    blood_group = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.patient_name} (ID: {self.Patient_id})"


class Appointment(models.Model):
    Appointment_id = models.AutoField(primary_key=True)
    token = models.CharField(max_length=20)
    appointment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="Scheduled")

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    # Fix: use string reference, not import
    doctor = models.ForeignKey(
        "admins.Doctor",
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return f"Appointment {self.Appointment_id} - {self.patient.patient_name}"


class ConsultationBill(models.Model):
    ConsultationBill_id = models.AutoField(primary_key=True)

    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)

    # Fix: use string reference
    consultation = models.ForeignKey(
        "doctor.Consultation",
        on_delete=models.CASCADE
    )

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    bill_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Consult Bill {self.ConsultationBill_id}"

from django.db import models
from django.contrib.auth.models import User

class Specialization(models.Model):
    spec_Id = models.AutoField(primary_key=True)
    specialization_name = models.CharField(max_length=30)

    def __str__(self):
        return self.specialization_name

class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    # From tblstaff
    # This links your staff profile to a Django login User
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    full_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    joining_date = models.DateField()
    mobile_number = models.CharField(max_length=10, unique=True)
    
    # The 'role' (e.g., 'Doctor', 'reception') is handled 
    # by adding the User to a Django "Group", so role_id is not needed.

    def __str__(self):
        return self.full_name

class Doctor(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    # From tbldoctor
    # This links the Doctor-specific details to a Staff profile
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE)
    
    consultation_fee = models.IntegerField()
    availability = models.CharField(max_length=30)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE) # <-- Field name is 'specialization'
    def __str__(self):
        # Access the full_name from the related Staff model
        return f"Dr. {self.staff.full_name}"
from django.contrib import admin
from .models import Patient, Appointment, ConsultationBill

admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(ConsultationBill)

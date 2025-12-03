from django.contrib import admin
from .models import Specialization, Staff, Doctor

# Register your models here.
admin.site.register(Specialization)
admin.site.register(Staff)
admin.site.register(Doctor)
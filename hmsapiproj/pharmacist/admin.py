from django.contrib import admin
from .models import Medicine, pharmacistBill, pharmacistBillItem

admin.site.register(Medicine)
admin.site.register(pharmacistBill)
admin.site.register(pharmacistBillItem)

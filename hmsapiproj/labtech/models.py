from django.db import models
from doctor.models import LabTestOrder


class LabTestCategory(models.Model):
    LabTestCategory_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=30)

    def __str__(self):
        return self.category_name


class LabTestParameter(models.Model):
    LabTestParameter_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(LabTestCategory, on_delete=models.CASCADE)
    label = models.CharField(max_length=30)
    normal_range = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.label} ({self.category.category_name})"


class LabReport(models.Model):
    LabReport_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(LabTestOrder, on_delete=models.CASCADE)
    category = models.ForeignKey(LabTestCategory, on_delete=models.PROTECT)
    report_date = models.DateField(auto_now_add=True)
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Lab Report {self.LabReport_id}"


class LabReportResult(models.Model):
    LabReportResult_id = models.AutoField(primary_key=True)
    report = models.ForeignKey(LabReport, on_delete=models.CASCADE, related_name="results")
    parameter = models.ForeignKey(LabTestParameter, on_delete=models.PROTECT)
    value = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.parameter.label} -> {self.value}"


class LabBill(models.Model):
    LabBill_id = models.AutoField(primary_key=True)
    bill_date = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    patient = models.ForeignKey("receptionist.Patient", on_delete=models.CASCADE)   # FIXED

    def __str__(self):
        return f"Lab Bill {self.LabBill_id}"


class LabBillItem(models.Model):
    LabBillItem_id = models.AutoField(primary_key=True)
    bill = models.ForeignKey(LabBill, on_delete=models.CASCADE, related_name="items")
    test = models.ForeignKey(LabTestCategory, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.test.category_name} - {self.subtotal}"



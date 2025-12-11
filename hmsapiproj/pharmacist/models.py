from django.db import models


class Medicine(models.Model):
    Medicine_id = models.AutoField(primary_key=True, serialize=False)
    # From tblmedicine
    medicine_name = models.CharField(max_length=30)
    manufacture_name = models.CharField(max_length=30)
    dosage = models.CharField(max_length=10)  # e.g., "500mg"
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.medicine_name} ({self.dosage})"


class pharmacistBill(models.Model):
    pharmacistBill_id = models.AutoField(primary_key=True, serialize=False)
    # This is the "Header" of your tblpharmacist_Bill
    bill_date = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    patient = models.ForeignKey(
        'receptionist.Patient',   # ← FIXED: was 'reception.Patient'
        on_delete=models.CASCADE
    )

    consultation = models.ForeignKey(
        'doctor.Consultation',
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return f"Bill {self.pharmacistBill_id} for {self.patient.patient_name}"


class pharmacistBillItem(models.Model):
    pharmacistBillItem_id = models.AutoField(primary_key=True, serialize=False)
    # This is the new "Lines" table that holds the individual medicines for a bill
    bill = models.ForeignKey(
        pharmacistBill,
        on_delete=models.CASCADE,
        related_name="items"  # Lets you get all items for a bill
    )
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.PROTECT
    )
    quantity = models.IntegerField()
    price_at_time_of_sale = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.medicine.medicine_name} for Bill {self.bill.pharmacistBill_id}"


class MedicineStock(models.Model):
    MedicineStock_id = models.AutoField(primary_key=True, serialize=False)
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE
    )
    quantity_in_stock = models.IntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    Reorder_level = models.IntegerField()
    Created_Date = models.DateField()

    def __str__(self):
        return f"{self.quantity} x {self.medicine.medicine_name}"
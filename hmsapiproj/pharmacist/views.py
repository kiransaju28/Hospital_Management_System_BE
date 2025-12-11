from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from admins.permissions import IsPharmacist
from .models import Medicine, pharmacistBill, MedicineStock, pharmacistBillItem
from .serializers import MedicineSerializer, pharmacistBillSerializer, MedicineStockSerializer
from admins.permissions import IsAdmin,IsDoctor


# --- Import Doctor models for the workflow ---
from doctor.models import Consultation
from doctor.serializers import ConsultationSerializer


class MedicineViewSet(viewsets.ModelViewSet):
    """
    Manage Inventory (Add/Edit/Delete medicines).
    Only Pharmacists can do this.
    """
    permission_classes = [IsPharmacist | IsAdmin|IsDoctor]
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['medicine_name']


class PendingPrescriptionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    WORKFLOW: Shows consultations where the doctor ordered medicines
    ('fulfill_pharmacist_internally'=True) but they haven't been billed yet.
    This is the Pharmacist's "To-Do List".
    """
    permission_classes = [IsPharmacist | IsAdmin|IsDoctor]
    serializer_class = ConsultationSerializer  # Re-use the doctor's serializer to see the meds

    def get_queryset(self):
        # 1. Doctor said "Internal pharmacist"
        # 2. Has prescription items
        # 3. NOT in pharmacistBill table yet (simplified check)

        # Get IDs of consultations that are already billed
        billed_ids = pharmacistBill.objects.values_list('consultation_id', flat=True)

        return Consultation.objects.filter(
            fulfill_pharmacist_internally=True,
            prescription_items__isnull=False
        ).exclude(consultation_id__in=billed_ids).distinct().order_by('consultation_id')


from django.db import transaction
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

def calculate_quantity(frequency, duration):
    """
    Parses frequency (e.g., '1-0-1') and duration (e.g., '5 days')
    to calculate total quantity required.
    """
    try:
        # Parse Frequency (1-0-1 -> 2)
        freq_parts = frequency.split('-')
        daily_count = sum(int(p) for p in freq_parts)
    except (ValueError, AttributeError):
        # Fallback or error if format is completely wrong
        # For now, let's treat 0 to avoid breaking, or raise error
        daily_count = 0

    try:
        # Parse Duration ('5 days' -> 5)
        # Taking first part and converting to int
        days = int(duration.split()[0])
    except (ValueError, IndexError, AttributeError):
        days = 0
    
    return daily_count * days


class pharmacistBillViewSet(viewsets.ModelViewSet):
    """
    Generate Bills.
    When a bill is created, it automatically subtracts stock (via Serializer or View logic).
    """
    permission_classes = [IsPharmacist | IsAdmin | IsDoctor]
    queryset = pharmacistBill.objects.all().order_by('pharmacistBill_id')
    serializer_class = pharmacistBillSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['patient__patient_name']

    def create(self, request, *args, **kwargs):
        consultation_id = request.data.get('consultation_id')
        if not consultation_id:
            raise ValidationError({"consultation_id": "This field is required."})

        try:
            consultation = Consultation.objects.get(pk=consultation_id)
        except Consultation.DoesNotExist:
            raise ValidationError({"consultation_id": "Consultation not found."})

        # 1. Fetch Prescription Items
        prescription_items = consultation.prescription_items.all()
        if not prescription_items.exists():
            raise ValidationError("No prescription items found for this consultation.")

        # 2. Calculate Requirements & Verify Stock
        # We'll store the calculated data to avoid re-looping complex logic
        # format: { 'medicine_obj': med, 'required_qty': 10, 'price_per_unit': 5.5 }
        items_to_process = []
        total_bill_amount = 0

        for item in prescription_items:
            qty = calculate_quantity(item.frequency, item.duration)
            if qty <= 0:
                raise ValidationError(f"Invalid quantity calculated for {item.medicine.medicine_name}. Check frequency/duration formats.")
            
            # Check Stock
            total_stock = MedicineStock.objects.filter(medicine=item.medicine).aggregate(total=Sum('quantity_in_stock'))['total'] or 0
            
            if total_stock < qty:
                raise ValidationError(f"Insufficient stock for {item.medicine.medicine_name}. Required: {qty}, Available: {total_stock}")

            items_to_process.append({
                'medicine': item.medicine,
                'required_qty': qty,
                'price_per_unit': item.medicine.price_per_unit
            })

        # 3. Atomic Transaction: Deduct Stock & Create Bill
        with transaction.atomic():
            # Create Bill Header
            # Note: We need the patient. Consultation -> Appointment -> Patient
            patient = consultation.appointment.patient
            
            bill = pharmacistBill.objects.create(
                patient=patient,
                consultation=consultation,
                total_amount=0  # Will update after calculating
            )

            bill_items_response = []

            for data in items_to_process:
                med = data['medicine']
                qty_needed = data['required_qty']
                price = data['price_per_unit']
                
                # --- Stock Deduction (FIFO) ---
                stocks = MedicineStock.objects.filter(medicine=med, quantity_in_stock__gt=0).order_by('Created_Date')
                
                temp_qty = qty_needed
                for stock_entry in stocks:
                    if temp_qty <= 0:
                        break
                    
                    if stock_entry.quantity_in_stock >= temp_qty:
                        stock_entry.quantity_in_stock -= temp_qty
                        stock_entry.save()
                        temp_qty = 0
                    else:
                        # Take all from this batch
                        temp_qty -= stock_entry.quantity_in_stock
                        stock_entry.quantity_in_stock = 0
                        stock_entry.save()

                # Double check to ensure we deducted enough (should be covered by initial check, but safety net)
                if temp_qty > 0:
                     raise ValidationError(f"Concurrency error: Stock changed during processing for {med.medicine_name}.")

                # --- Create Bill Item ---
                subtotal = qty_needed * price
                total_bill_amount += subtotal
                
                pharmacistBillItem.objects.create(
                    bill=bill,
                    medicine=med,
                    quantity=qty_needed,
                    price_at_time_of_sale=price,
                    subtotal=subtotal
                )

                bill_items_response.append({
                    "medicine": med.medicine_name,
                    "qty": qty_needed,
                    "price": float(subtotal)
                })

            # Update final total
            bill.total_amount = total_bill_amount
            bill.save()

        # 4. Return Custom Response
        return Response({
            "message": "Bill created successfully",
            "bill_id": bill.pharmacistBill_id,
            "total_amount": float(total_bill_amount),
            "items": bill_items_response
        }, status=status.HTTP_201_CREATED)


class MedicineStockViewSet(viewsets.ModelViewSet):
    """
    Manage Medicine Stock (Add/Edit/Delete stock entries).
    """
    permission_classes = [IsPharmacist | IsAdmin | IsDoctor]
    queryset = MedicineStock.objects.all()
    serializer_class = MedicineStockSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['medicine__medicine_name']


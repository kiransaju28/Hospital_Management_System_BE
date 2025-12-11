from rest_framework import serializers
from .models import Medicine, pharmacistBill, pharmacistBillItem, MedicineStock
import pharmacist.models as models # ensuring models is available if needed, though direct import is better


# =======================
# MEDICINE SERIALIZER
# =======================
class MedicineSerializer(serializers.ModelSerializer):
    quantity_in_stock = serializers.SerializerMethodField()

    class Meta:
        model = Medicine
        fields = '__all__'

    def get_quantity_in_stock(self, obj):
        # Sum up all stocks for this medicine
        stocks = models.MedicineStock.objects.filter(medicine=obj)
        return sum(s.quantity_in_stock for s in stocks)


# =======================
# pharmacist BILL ITEM
# =======================
class pharmacistBillItemSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.medicine_name', read_only=True)

    class Meta:
        model = pharmacistBillItem
        fields = [
            'pharmacistBillItem_id',
            'medicine',
            'medicine_name',
            'quantity',
            'price_at_time_of_sale',
            'subtotal'
        ]
        read_only_fields = ['price_at_time_of_sale', 'subtotal']


# =======================
# pharmacist BILL (MAIN)
# =======================
class pharmacistBillSerializer(serializers.ModelSerializer):
    items = pharmacistBillItemSerializer(many=True)

    class Meta:
        model = pharmacistBill
        fields = [
            'pharmacistBill_id',
            'bill_date',
            'total_amount',
            'patient',
            'consultation',
            'items'
        ]
        read_only_fields = ['bill_date', 'total_amount']

    def create(self, validated_data):
        items_data = validated_data.pop('items')

        # Create bill header
        bill = pharmacistBill.objects.create(total_amount=0, **validated_data)

        total_amount = 0

        for item_data in items_data:
            medicine = item_data['medicine']
            quantity_needed = item_data['quantity']
            original_quantity_needed = quantity_needed

            # 1. Check Total Stock Available across all batches
            stocks = models.MedicineStock.objects.filter(medicine=medicine).order_by('Created_Date')
            total_available = sum(stock.quantity_in_stock for stock in stocks)

            if total_available < quantity_needed:
                raise serializers.ValidationError(
                    f"Not enough stock for {medicine.medicine_name}. "
                    f"Requested: {quantity_needed}, Available: {total_available}"
                )

            # 2. FIFO Stock Deduction
            for stock in stocks:
                if quantity_needed <= 0:
                    break
                
                if stock.quantity_in_stock <= quantity_needed:
                    # Determine how much we take from this batch
                    taken = stock.quantity_in_stock
                    quantity_needed -= taken
                    # This batch is empty, delete it? Or keep it at 0? 
                    # Usually deleting or archiving is better to keep table clean, 
                    # but for history let's just delete or set to 0. 
                    # Use case: Delete if empty to avoid iterating empty rows.
                    stock.delete() 
                else:
                    # Batch has more than needed
                    stock.quantity_in_stock -= quantity_needed
                    stock.save()
                    quantity_needed = 0

            price = medicine.price_per_unit
            subtotal = price * original_quantity_needed

            # Save item
            pharmacistBillItem.objects.create(
                bill=bill,
                medicine=medicine,
                quantity=original_quantity_needed,
                price_at_time_of_sale=price,
                subtotal=subtotal
            )

            total_amount += subtotal

        bill.total_amount = total_amount
        bill.save()

        return bill


# =======================
# MEDICINE STOCK SERIALIZER
# =======================
class MedicineStockSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.medicine_name', read_only=True)

    class Meta:
        model = models.MedicineStock  # We need to ensure 'models' is imported correctly or import MedicineStock
        fields = [
            'MedicineStock_id',
            'medicine',
            'medicine_name',
            'quantity_in_stock',
            'purchase_price',
            'Reorder_level',
            'Created_Date'
        ]


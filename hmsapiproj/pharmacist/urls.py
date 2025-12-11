from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MedicineViewSet,
    pharmacistBillViewSet,
    PendingPrescriptionViewSet,  # <-- To-Do list
    MedicineStockViewSet,
)

router = DefaultRouter()
router.register(r'medicines', MedicineViewSet)
router.register(r'bills', pharmacistBillViewSet)
router.register(
    r'pending-prescriptions',
    PendingPrescriptionViewSet,
    basename='pending-prescriptions'
)
router.register(r'medicine-stock', MedicineStockViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

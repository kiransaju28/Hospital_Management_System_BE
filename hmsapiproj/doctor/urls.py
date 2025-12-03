from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    TodayAppointmentsViewSet,
    BasicVitalsViewSet,
    ConsultationViewSet,
    PrescriptionItemViewSet,
    LabTestOrderViewSet,
)

router = DefaultRouter()
router.register(r"today-appointments", TodayAppointmentsViewSet, basename="today-appointments")
router.register(r"basic-vitals", BasicVitalsViewSet)
router.register(r"consultations", ConsultationViewSet)
router.register(r"prescription-items", PrescriptionItemViewSet)
router.register(r"lab-test-orders", LabTestOrderViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

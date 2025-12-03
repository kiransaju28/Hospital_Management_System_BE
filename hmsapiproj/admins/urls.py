from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterUserViewSet,
    StaffViewSet,
    DoctorViewSet,
    SpecializationViewSet,
)

router = DefaultRouter()
router.register(r"register-user", RegisterUserViewSet, basename="register-user")
router.register(r"staff", StaffViewSet)
router.register(r"doctors", DoctorViewSet)
router.register(r"specializations", SpecializationViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

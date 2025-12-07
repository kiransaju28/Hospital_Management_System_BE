from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from admins.permissions import Islabtech

from .models import (
    LabTestCategory,
    LabTestParameter,
    LabReport,
    LabReportResult,
    LabBill,
    LabBillItem,
)
from .serializers import (
    LabTestCategorySerializer,
    LabTestParameterSerializer,
    LabReportSerializer,
    LabReportResultSerializer,
    LabBillSerializer,
    LabBillItemSerializer,
)

from doctor.models import LabTestOrder
from doctor.serializers import LabTestOrderSerializer


# --------------------------
# CATEGORY
# --------------------------
class LabTestCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = LabTestCategory.objects.all()
    serializer_class = LabTestCategorySerializer


class LabTestParameterViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = LabTestParameter.objects.all()
    serializer_class = LabTestParameterSerializer


# --------------------------
# PENDING TEST ORDERS
# --------------------------
class PendingLabTestsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = LabTestOrder.objects.all()
    serializer_class = LabTestOrderSerializer


# --------------------------
# LAB REPORT
# --------------------------
class LabReportViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = LabReport.objects.all()
    serializer_class = LabReportSerializer


class LabReportResultViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = LabReportResult.objects.all()
    serializer_class = LabReportResultSerializer


# --------------------------
# LAB BILL
# --------------------------
class LabBillViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = LabBill.objects.all()
    serializer_class = LabBillSerializer


class LabBillItemViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = LabBillItem.objects.all()
    serializer_class = LabBillItemSerializer

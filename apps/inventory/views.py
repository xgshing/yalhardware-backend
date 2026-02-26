# apps/inventory/views.py
from rest_framework import viewsets, permissions
from .models import InventoryRecord
from .serializers import InventoryRecordSerializer


class InventoryRecordViewSet(viewsets.ReadOnlyModelViewSet):
    """
    库存流水（只允许后台查看）
    """

    queryset = InventoryRecord.objects.select_related(
        "variant", "variant_product"
    ).order_by("-created_at")

    serializer_class = InventoryRecordSerializer
    permission_classes = [permissions.IsAdminUser]

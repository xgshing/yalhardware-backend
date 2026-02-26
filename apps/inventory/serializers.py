# apps/inventory/serializers.py
from rest_framework import serializers
from .models import InventoryRecord


class InventoryRecordSerializer(serializers.ModelSerializer):
    variant_id = serializers.IntegerField(source="variant.id", read_only=True)
    product_name = serializers.CharField(source="variant.product.name", read_only=True)
    variant_spec = serializers.CharField(source="variant.spec", read_only=True)

    class Meta:
        model = InventoryRecord
        fields = [
            "id",
            "variant_id",
            "product_name",
            "variant_spec",
            "action",
            "quantity",
            "remark",
            "operator",
            "created_at",
        ]

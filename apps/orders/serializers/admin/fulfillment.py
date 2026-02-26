# apps/orders/serializers/admin/fulfillment.py
from rest_framework import serializers
from apps.orders.models import Fulfillment, FulfillmentItem


class FulfillmentItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(
        source="order_item.product_title", read_only=True
    )

    class Meta:
        model = FulfillmentItem
        fields = ["id", "product_title", "quantity"]


class AdminFulfillmentSerializer(serializers.ModelSerializer):
    items = FulfillmentItemSerializer(many=True, read_only=True)

    class Meta:
        model = Fulfillment
        fields = [
            "id",
            "carrier",
            "tracking_no",
            "status",
            "shipped_at",
            "items",
        ]

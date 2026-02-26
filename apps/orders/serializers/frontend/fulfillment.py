# apps/orders/serializers/frontend/fulfillment.py
# apps/orders/serializers/fulfillment.py
from rest_framework import serializers
from apps.orders.models import Fulfillment, FulfillmentItem
from .order_item import OrderItemSerializer


class FulfillmentItemSerializer(serializers.ModelSerializer):
    order_item = OrderItemSerializer(read_only=True)

    class Meta:
        model = FulfillmentItem
        fields = ["id", "order_item", "quantity"]


class FulfillmentSerializer(serializers.ModelSerializer):
    items = FulfillmentItemSerializer(many=True, read_only=True)
    operator_name = serializers.CharField(source="operator.username", read_only=True)

    class Meta:
        model = Fulfillment
        fields = [
            "id",
            "carrier",
            "tracking_no",
            "status",
            "shipped_at",
            "operator_name",
            "items",
        ]

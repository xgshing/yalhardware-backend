# apps/orders/serializers/order_item.py
from rest_framework import serializers
from apps.orders.models import OrderItem


class AdminOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product_title",
            "sku_title",
            "quantity",
            "price",
        ]

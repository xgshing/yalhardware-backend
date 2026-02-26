# 后台订单详情 Serializer
# apps/orders/serializers/admin/order_detail.py
from rest_framework import serializers
from apps.orders.models import Order
from .order_item import AdminOrderItemSerializer
from .fulfillment import AdminFulfillmentSerializer
from apps.orders.services.order_actions import get_available_actions


class AdminOrderDetailSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)
    items = AdminOrderItemSerializer(many=True, read_only=True)
    fulfillments = AdminFulfillmentSerializer(many=True, read_only=True)
    actions = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "order_no",
            "status",
            "total_amount",
            "created_at",
            "paid_at",
            "user_email",
            "items",
            "fulfillments",
            "actions",
        ]

    def get_actions(self, obj):
        return get_available_actions(obj)

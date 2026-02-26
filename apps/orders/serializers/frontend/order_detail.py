# 订单详情专用
# apps/orders/serializers/order_detail.py
from rest_framework import serializers
from apps.orders.models import Order
from .order_item import OrderItemSerializer
from .fulfillment import FulfillmentSerializer


class OrderDetailSerializer(serializers.ModelSerializer):
    status = serializers.CharField()
    status_label = serializers.CharField(source="get_status_display")
    items = OrderItemSerializer(many=True)
    fulfillments = FulfillmentSerializer(many=True, read_only=True)  # 多条发货物流

    can_cancel = serializers.SerializerMethodField()
    can_pay = serializers.SerializerMethodField()
    can_confirm = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "order_no",
            "status",
            "status_label",
            "total_amount",
            "created_at",
            "paid_at",
            "shipped_at",
            "completed_at",
            "items",
            "fulfillments",
            "can_cancel",
            "can_pay",
            "can_confirm",
        ]

    def get_can_cancel(self, obj):
        return obj.status == Order.Status.PENDING

    def get_can_pay(self, obj):
        return obj.status == Order.Status.PENDING

    def get_can_confirm(self, obj):
        return obj.status == Order.Status.SHIPPED

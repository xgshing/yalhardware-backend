# 后台订单列表 Serializer
# apps/orders/serializers/admin/order_list.py
from rest_framework import serializers
from apps.orders.models import Order
from apps.orders.services.order_actions import get_available_actions


class AdminOrderListSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)
    actions = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "order_no",
            "status",
            "total_amount",
            "created_at",
            "user_email",
            "actions",
        ]

    def get_actions(self, obj):
        return get_available_actions(obj)

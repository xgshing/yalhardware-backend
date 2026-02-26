# 后台订单详情API
# apps/orders/views/admin/order_detail.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from apps.orders.models import Order
from apps.orders.serializers.admin.order_detail import AdminOrderDetailSerializer


class AdminOrderDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        serializer = AdminOrderDetailSerializer(order)
        return Response(serializer.data)

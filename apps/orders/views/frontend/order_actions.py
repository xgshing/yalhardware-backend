# 订单行为接口（取消 / 支付 / 确认收货）
# apps/orders/views/frontend/order_actions.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from apps.orders.models import Order
from apps.orders.services.order_state_service import OrderStateService


class OrderCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        OrderStateService.cancel(order)
        return Response({"status": "ok"})


class OrderPayView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        OrderStateService.pay(order)
        return Response({"status": "paid"})


class OrderConfirmView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        OrderStateService.confirm(order)
        return Response({"status": "completed"})

# 发货 API
# apps/orders/views/admin/order_ship.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.shortcuts import get_object_or_404

from apps.orders.models import Order, Fulfillment, FulfillmentItem
from apps.orders.services.order_state_service import OrderStateService


class AdminOrderShipView(APIView):
    permission_classes = [IsAdminUser]

    @transaction.atomic
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)

        if order.status != Order.Status.PAID:
            return Response(
                {"detail": "当前订单不可发货"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        carrier = request.data.get("carrier")
        tracking_no = request.data.get("tracking_no")
        items = request.data.get("items", [])

        fulfillment = Fulfillment.objects.create(
            order=order,
            carrier=carrier,
            tracking_no=tracking_no,
            operator=request.user,
        )

        for item in items:
            FulfillmentItem.objects.create(
                fulfillment=fulfillment,
                order_item_id=item["order_item_id"],
                quantity=item["quantity"],
            )

        OrderStateService.ship(order)

        return Response({"status": "shipped"})

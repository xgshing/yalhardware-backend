# 订单详情接口
# apps/orders/views/frontend/order_detail.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from apps.orders.models import Order
from apps.orders.serializers.frontend.order_detail import OrderDetailSerializer


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        """
        订单详情
        """
        order = get_object_or_404(
            Order.objects.prefetch_related(
                "items",
                "items__review",
                "items__review__reply",
            ),
            id=order_id,
            user=request.user,
        )

        serializer = OrderDetailSerializer(
            order,
            context={"request": request},
        )
        return Response(serializer.data)

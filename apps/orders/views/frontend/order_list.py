# 前台用户订单列表 API
# apps/orders/views/frontend/order_list.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.orders.models import Order
from apps.orders.serializers.frontend.order_list import OrderListSerializer


class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        我的订单列表
        """
        qs = (
            Order.objects.filter(user=request.user)
            .prefetch_related(
                "items",
                "items__review",
                "items__review__reply",
            )
            .order_by("-created_at")
        )

        serializer = OrderListSerializer(
            qs,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

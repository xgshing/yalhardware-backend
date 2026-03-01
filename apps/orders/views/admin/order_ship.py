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
    """
    后台管理员发货接口
    """

    permission_classes = [IsAdminUser]

    @transaction.atomic
    def post(self, request, order_id):
        # 获取订单
        order = get_object_or_404(Order, id=order_id)

        # 校验订单状态
        if order.status != Order.Status.PAID:
            return Response(
                {"detail": "当前订单不可发货"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 从请求里获取参数
        carrier = request.data.get("carrier")
        tracking_no = request.data.get("tracking_no")
        items = request.data.get("items")

        # 参数校验
        if not carrier:
            return Response(
                {"detail": "请提供物流公司"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not tracking_no:
            return Response(
                {"detail": "请提供运单号"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not items or not isinstance(items, list):
            return Response(
                {"detail": "请提供有效的发货商品列表"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # 创建发货记录
            fulfillment = Fulfillment.objects.create(
                order=order,
                carrier=carrier,
                tracking_no=tracking_no,
                operator=request.user,
            )

            # 创建发货明细
            for item in items:
                order_item_id = item.get("order_item_id")
                quantity = item.get("quantity")
                if not order_item_id or quantity is None:
                    # 非法数据直接回滚
                    raise ValueError("发货明细缺少 order_item_id 或 quantity")
                FulfillmentItem.objects.create(
                    fulfillment=fulfillment,
                    order_item_id=order_item_id,
                    quantity=quantity,
                )

            # 调用订单状态服务更新订单状态
            OrderStateService.ship(order, carrier, tracking_no, items)

        except Exception as e:
            # 捕获异常，事务回滚
            return Response(
                {"detail": f"发货失败: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # 成功返回
        return Response({"status": "shipped"})

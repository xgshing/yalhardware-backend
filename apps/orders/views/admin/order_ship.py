# 发货 API
# apps/orders/views/admin/order_ship.py

from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from django.db import transaction, IntegrityError
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from apps.orders.models import Order, OrderItem
from apps.orders.services.order_state_service import OrderStateService


class AdminOrderShipView(APIView):
    """
    后台管理员发货接口（生产级版本）

    特性：
    - 行级锁防并发
    - 严格参数校验
    - 校验发货明细归属
    - 统一通过 OrderStateService 处理业务
    - 精准异常返回
    """

    permission_classes = [IsAdminUser]

    @transaction.atomic
    def post(self, request, order_id):

        # 行级锁，防止并发重复发货
        order = get_object_or_404(
            Order.objects.select_for_update(),
            id=order_id,
        )

        carrier = request.data.get("carrier")
        tracking_no = request.data.get("tracking_no")
        items = request.data.get("items")

        # ================= 参数校验 =================

        if not carrier or not isinstance(carrier, str):
            return Response(
                {"detail": "请提供有效的物流公司"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not tracking_no or not isinstance(tracking_no, str):
            return Response(
                {"detail": "请提供有效的运单号"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not items or not isinstance(items, list):
            return Response(
                {"detail": "请提供有效的发货商品列表"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        validated_items = []

        for item in items:
            if not isinstance(item, dict):
                return Response(
                    {"detail": "发货明细格式错误"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            order_item_id = item.get("order_item_id")
            quantity = item.get("quantity")

            if not order_item_id or quantity is None:
                return Response(
                    {"detail": "发货明细缺少 order_item_id 或 quantity"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not isinstance(quantity, int) or quantity <= 0:
                return Response(
                    {"detail": "发货数量必须为正整数"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # 校验该商品是否属于当前订单
            order_item = get_object_or_404(
                OrderItem,
                id=order_item_id,
                order=order,
            )

            # 防止超发
            if quantity > order_item.quantity:
                return Response(
                    {"detail": f"商品 {order_item.product_title} 发货数量超出购买数量"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            validated_items.append(
                {
                    "order_item_id": order_item.id,
                    "quantity": quantity,
                }
            )

        # ================= 业务执行 =================

        try:
            OrderStateService.ship(
                order=order,
                carrier=carrier.strip(),
                tracking_no=tracking_no.strip(),
                items=validated_items,
                operator=request.user,
            )

        except ValidationError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except IntegrityError:
            # 一般用于数据库唯一约束冲突（建议在 Fulfillment 加 unique(order, tracking_no)）
            return Response(
                {"detail": "该运单号已存在，不能重复发货"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception:
            # 不暴露内部错误
            return Response(
                {"detail": "发货失败，请联系管理员"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {"status": "shipped"},
            status=status.HTTP_200_OK,
        )

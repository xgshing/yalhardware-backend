# 前台用户创建订单
# apps/orders/views/frontend/order_submit.py

from decimal import Decimal
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from apps.orders.models import Order, OrderItem
from apps.products.models import ProductVariant
from apps.orders.utils.order_no import generate_order_no


class OrderSubmitView(APIView):
    """
    前台用户提交订单（购物车 → 订单）
    """

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        user = request.user
        items = request.data.get("items", [])

        # ===============================
        # 0️⃣ 参数校验
        # ===============================
        if not items or not isinstance(items, list):
            return Response(
                {"detail": "订单商品不能为空"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ===============================
        # 1️⃣ 创建订单主表（金额先占位）
        # ===============================
        order = Order.objects.create(
            user=user,
            order_no=generate_order_no(),
            status=Order.Status.PENDING,
            total_amount=Decimal("0.00"),
        )

        total_amount = Decimal("0.00")

        # ===============================
        # 2️⃣ 创建订单商品行（锁库存）
        # ===============================
        for item in items:
            variant_id = item.get("variant_id")
            quantity = int(item.get("quantity", 0))

            if not variant_id or quantity <= 0:
                return Response(
                    {"detail": "订单商品参数错误"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # 锁定 SKU，防止并发超卖
            variant = (
                ProductVariant.objects.select_for_update()
                .select_related("product")
                .get(id=variant_id)
            )

            if variant.stock < quantity:
                return Response(
                    {"detail": f"商品库存不足（SKU ID: {variant_id}）"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # 成交价来自 Product（与你模型一致）
            price = variant.product.price
            line_total = price * quantity
            total_amount += line_total

            # 扣库存
            variant.stock -= quantity
            variant.save(update_fields=["stock"])

            # 写入订单商品快照
            OrderItem.objects.create(
                order=order,
                product_id=variant.product.id,
                product_title=variant.product.name,
                product_image=variant.style_image,
                sku_title=variant.spec or variant.style_name or "",
                quantity=quantity,
                price=price,
            )

        # ===============================
        # 3️⃣ 回写订单总金额
        # ===============================
        order.total_amount = total_amount
        order.save(update_fields=["total_amount"])

        # ===============================
        # 4️⃣ 返回下单结果
        # ===============================
        return Response(
            {
                "id": order.id,
                "order_no": order.order_no,
                "status": order.status,
                "total_amount": str(order.total_amount),
                "created_at": order.created_at,
            },
            status=status.HTTP_201_CREATED,
        )

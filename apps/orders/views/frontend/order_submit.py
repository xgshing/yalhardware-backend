# 前台用户创建订单
# apps/orders/views/frontend/order_submit.py

from decimal import Decimal, InvalidOperation
from django.db import transaction
from django.db.models import F
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from apps.orders.models import Order, OrderItem
from apps.products.models import ProductVariant
from apps.orders.utils.order_no import generate_order_no


class OrderSubmitView(APIView):
    """
    前台用户提交订单（购物车 → 订单）

    生产级版本：
    - 严格参数校验
    - 原子事务保证
    - SKU锁定防超卖
    - 不创建空订单
    - 全量异常回滚
    """

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        user = request.user
        items = request.data.get("items")

        # ===============================
        # 1️⃣ 基础参数校验
        # ===============================
        if not isinstance(items, list) or len(items) == 0:
            raise ValidationError({"detail": "订单商品不能为空"})

        validated_items = []

        for idx, item in enumerate(items):
            if not isinstance(item, dict):
                raise ValidationError({"detail": f"第{idx+1}项商品参数格式错误"})

            variant_id = item.get("variant_id")
            quantity = item.get("quantity")

            if variant_id is None or quantity is None:
                raise ValidationError({"detail": "订单商品参数缺失"})

            try:
                variant_id = int(variant_id)
                quantity = int(quantity)
            except (ValueError, TypeError):
                raise ValidationError({"detail": "订单商品参数类型错误"})

            if quantity <= 0:
                raise ValidationError({"detail": "商品数量必须大于0"})

            validated_items.append(
                {
                    "variant_id": variant_id,
                    "quantity": quantity,
                }
            )

        # ===============================
        # 2️⃣ 锁定SKU并计算金额
        # ===============================
        total_amount = Decimal("0.00")
        order_items_data = []

        for item in validated_items:
            variant_id = item["variant_id"]
            quantity = item["quantity"]

            try:
                variant = (
                    ProductVariant.objects.select_for_update()
                    .select_related("product")
                    .get(id=variant_id)
                )
            except ProductVariant.DoesNotExist:
                raise ValidationError({"detail": f"商品不存在（SKU ID: {variant_id}）"})

            if variant.stock < quantity:
                raise ValidationError(
                    {"detail": f"商品库存不足（SKU ID: {variant_id}）"}
                )

            price = variant.product.price

            try:
                price = Decimal(price)
            except (InvalidOperation, TypeError):
                raise ValidationError({"detail": "商品价格异常，请联系管理员"})

            line_total = price * quantity
            total_amount += line_total

            order_items_data.append(
                {
                    "variant": variant,
                    "quantity": quantity,
                    "price": price,
                    "line_total": line_total,
                }
            )

        # ===============================
        # 3️⃣ 创建订单主表
        # ===============================
        order = Order.objects.create(
            user=user,
            order_no=generate_order_no(),
            status=Order.Status.PENDING,
            total_amount=total_amount,
            created_at=timezone.now(),
        )

        # ===============================
        # 4️⃣ 创建订单商品 & 扣库存
        # ===============================
        for data in order_items_data:
            variant = data["variant"]
            quantity = data["quantity"]
            price = data["price"]

            # 扣库存（数据库级原子扣减）
            updated = ProductVariant.objects.filter(
                id=variant.id, stock__gte=quantity
            ).update(stock=F("stock") - quantity)

            if updated == 0:
                raise ValidationError(
                    {"detail": f"商品库存不足（SKU ID: {variant.id}）"}
                )

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
        # 5️⃣ 返回响应
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

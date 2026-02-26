# 订单状态机 / 行为规则
# apps/orders/services/order_state_service.py
from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ValidationError

from apps.orders.models import Order
from apps.orders.models.fulfillment import Fulfillment
from apps.orders.models.fulfillment_item import FulfillmentItem


class OrderStateService:
    """
    订单状态流转唯一入口（上线冻结）
    支持多条发货记录
    """

    @staticmethod
    def cancel(order: Order):
        if order.status != Order.Status.PENDING:
            raise ValidationError("当前订单状态不允许取消")
        order.status = Order.Status.CANCELLED
        order.save(update_fields=["status"])

    @staticmethod
    def pay(order: Order):
        if order.status != Order.Status.PENDING:
            raise ValidationError("当前订单状态不允许支付")
        order.status = Order.Status.PAID
        order.paid_at = timezone.now()
        order.save(update_fields=["status", "paid_at"])

    @staticmethod
    @transaction.atomic
    def ship(
        order: Order,
        carrier: str,
        tracking_no: str,
        items: list[dict],  # [{'order_item_id': int, 'quantity': int}]
        operator=None,
    ):
        """
        发货：
        - 创建 Fulfillment 记录
        - 创建 FulfillmentItem
        - 更新订单状态为 SHIPPED
        - 更新 order.shipped_at 为最近一次发货时间
        """
        if order.status not in [Order.Status.PAID, Order.Status.SHIPPED]:
            raise ValidationError("当前订单状态不允许发货")

        # 创建发货记录
        fulfillment = Fulfillment.objects.create(
            order=order,
            carrier=carrier,
            tracking_no=tracking_no,
            shipped_at=timezone.now(),
            operator=operator,
            status=Fulfillment.Status.SHIPPED,
        )

        # 创建发货明细
        for item in items:
            FulfillmentItem.objects.create(
                fulfillment=fulfillment,
                order_item_id=item["order_item_id"],
                quantity=item["quantity"],
            )

        # 更新订单状态和 shipped_at 为最近一次发货时间
        order.status = Order.Status.SHIPPED
        order.shipped_at = fulfillment.shipped_at
        order.save(update_fields=["status", "shipped_at"])

    @staticmethod
    def confirm(order: Order):
        if order.status != Order.Status.SHIPPED:
            raise ValidationError("当前订单状态不允许确认收货")
        order.status = Order.Status.COMPLETED
        order.completed_at = timezone.now()
        order.save(update_fields=["status", "completed_at"])

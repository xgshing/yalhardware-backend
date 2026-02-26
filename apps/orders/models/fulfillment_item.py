# 发货 / 履约模型
# apps/orders/models/fulfillment_item.py
from django.db import models
from .fulfillment import Fulfillment
from .order_item import OrderItem


class FulfillmentItem(models.Model):
    fulfillment = models.ForeignKey(
        Fulfillment,
        related_name="items",
        on_delete=models.CASCADE,
    )

    order_item = models.ForeignKey(
        OrderItem,
        on_delete=models.CASCADE,
    )

    quantity = models.PositiveIntegerField(verbose_name="发货数量")

    class Meta:
        db_table = "order_fulfillment_items"
        unique_together = ("fulfillment", "order_item")

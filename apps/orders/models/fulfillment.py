# 发货 / 履约模型
# apps/orders/models/fulfillment.py
from django.db import models
from django.conf import settings
from .order import Order


class Fulfillment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "待发货"
        SHIPPED = "SHIPPED", "已发货"
        DELIVERED = "DELIVERED", "已签收"

    order = models.ForeignKey(
        Order,
        related_name="fulfillments",
        on_delete=models.CASCADE,
        verbose_name="订单",
    )

    carrier = models.CharField(max_length=100, verbose_name="物流公司")
    tracking_no = models.CharField(max_length=100, verbose_name="运单号")

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SHIPPED,
    )

    shipped_at = models.DateTimeField(auto_now_add=True)
    operator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="操作人",
    )

    class Meta:
        db_table = "order_fulfillments"
        verbose_name = "订单发货"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.order.order_no} - {self.tracking_no}"

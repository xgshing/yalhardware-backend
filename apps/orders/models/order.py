# 订单主表
# apps/orders/models/order.py
from django.conf import settings
from django.db import models


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "待支付"
        PAID = "PAID", "已支付"
        SHIPPED = "SHIPPED", "已发货"
        COMPLETED = "COMPLETED", "已完成"
        CANCELLED = "CANCELLED", "已取消"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="下单用户",
    )

    order_no = models.CharField(
        max_length=32,
        unique=True,
        db_index=True,
        verbose_name="订单号",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="订单状态",
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="订单总金额",
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name="支付时间")
    shipped_at = models.DateTimeField(null=True, blank=True, verbose_name="发货时间")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="完成时间")

    class Meta:
        db_table = "orders"
        ordering = ["-created_at"]
        verbose_name = "订单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.order_no}"

# 订单行项目（Order 的子实体）
# apps/orders/models/order_item.py
from django.db import models
from .order import Order
from apps.products.models import Product


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="所属订单",
    )

    product = models.ForeignKey(
        Product,
        null=True,  # 可空
        blank=True,
        on_delete=models.SET_NULL,
        related_name="order_items",
        verbose_name="商品对象",
    )

    # 历史快照字段

    product_title = models.CharField(
        null=True, blank=True, max_length=255, verbose_name="商品标题"
    )
    product_image = models.URLField(
        null=True, blank=True, max_length=500, verbose_name="商品图片"
    )

    sku_title = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="SKU 描述",
    )

    quantity = models.PositiveIntegerField(verbose_name="购买数量")

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="成交单价",
    )

    class Meta:
        db_table = "order_items"
        verbose_name = "订单商品"
        verbose_name_plural = verbose_name
        unique_together = ("order", "product_id", "sku_title")

    def __str__(self):
        return f"{self.order.order_no} - {self.product_title or (self.product.name if self.product else '')}"

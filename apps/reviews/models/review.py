# 订单项评论（OneToOne）
# apps/reviews/models/review.py
from django.conf import settings
from django.db import models
from apps.orders.models.order_item import OrderItem


class Review(models.Model):
    order_item = models.OneToOneField(
        OrderItem,
        on_delete=models.CASCADE,
        related_name="review",
        verbose_name="订单商品",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="评价用户",
    )

    rating = models.PositiveSmallIntegerField(verbose_name="评分（1-5）")
    content = models.TextField(verbose_name="评价内容")
    images = models.JSONField(default=list, blank=True, verbose_name="评价图片")

    # 用户追加评价
    append_content = models.TextField(blank=True, default="", verbose_name="追评内容")
    append_at = models.DateTimeField(null=True, blank=True, verbose_name="追评时间")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="评价时间")

    class Meta:
        db_table = "reviews"
        verbose_name = "商品评价"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"Review #{self.id}"

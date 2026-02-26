# 商家回复
# apps/reviews/models/review_reply.py
from django.db import models
from .review import Review


class ReviewReply(models.Model):
    review = models.OneToOneField(
        Review,
        on_delete=models.CASCADE,
        related_name="reply",
        verbose_name="所属评价",
    )
    merchant_reply = models.TextField(blank=True, default="", verbose_name="商家回复")
    merchant_replied_at = models.DateTimeField(
        null=True, blank=True, verbose_name="商家回复时间"
    )

    class Meta:
        db_table = "review_replies"
        verbose_name = "商家回复"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"Reply for Review #{self.review_id}"

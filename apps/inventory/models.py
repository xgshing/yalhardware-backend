# 库存模型
# apps/inventory/models.py
from django.db import models
from django.conf import settings
from apps.products.models import ProductVariant


class InventoryRecord(models.Model):
    class Action(models.TextChoices):
        LOCK = "LOCK", "锁定库存"
        RELEASE = "RELEASE", "释放库存"
        DEDUCT = "DEDUCT", "扣减库存"
        ADJUST = "ADJUST", "人工调整"

    variant = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE, related_name="inventory_records"
    )

    action = models.CharField(max_length=20, choices=Action.choices)
    quantity = models.IntegerField()
    remark = models.CharField(max_length=255, blank=True)

    operator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.variant.id}{self.action}{self.quantity}"

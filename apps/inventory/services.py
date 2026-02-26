# apps/inventory/services.py
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import InventoryRecord


def lock_variant_stock(variant, quantity):
    """
    下单时锁库存
    """
    if variant.stock < quantity:
        raise ValidationError("库存不足")

    variant.stock -= quantity
    variant.save(update_fields=["stock"])

    InventoryRecord.objects.create(
        variant=variant,
        action=InventoryRecord.Action.LOCK,
        quantity=-quantity,
        remark="下单锁库存",
    )


def rollback_variant_stock(variant, quantity):
    """
    订单取消/超时释放库存
    """
    variant.stock += quantity
    variant.save(update_fields=["stock"])

    InventoryRecord.objects.create(
        variant=variant,
        action=InventoryRecord.Action.RELEASE,
        quantity=quantity,
        remark="订单取消释放库存",
    )


def rollback_order_stock(order):
    """
    回滚整个订单的库存
    """
    from apps.orders.models import OrderItem

    for item in OrderItem.objects.filter(order=order):
        rollback_variant_stock(item.variant, item.quantity)

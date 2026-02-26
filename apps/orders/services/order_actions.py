# 能力描述层
# apps/orders/services/order_actions.py
from apps.orders.models import Order


def get_available_actions(order: Order) -> list[str]:
    if order.status == Order.Status.PENDING:
        return ["pay", "cancel"]

    if order.status == Order.Status.PAID:
        return ["ship", "refund"]

    if order.status == Order.Status.SHIPPED:
        return ["confirm"]

    if order.status == Order.Status.COMPLETED:
        return ["review"]

    return []

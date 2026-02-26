# 订单状态与枚举
# apps/orders/constants.py


class OrderStatus:
    PENDING_PAY = "pending_pay"
    PAID = "paid"
    SHIPPED = "shipped"
    FINISHED = "finished"
    CLOSED = "closed"

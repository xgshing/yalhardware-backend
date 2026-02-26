# 订单号生成（雪花算法）
# apps/orders/utils/order_no.py
import time
import random


def generate_order_no(machine_id: int = 1):
    """
    时间戳 + 机器ID + 随机序列
    """
    timestamp = int(time.time() * 1000)
    sequence = random.randint(100, 999)
    return f"{timestamp}{machine_id:02d}{sequence}"

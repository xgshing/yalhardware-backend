# 后台订单列表API
# apps/orders/views/admin/order_list.py
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination
from apps.orders.models import Order
from apps.orders.serializers.admin.order_list import AdminOrderListSerializer
from apps.users.permissions import IsAdminUser as CustomIsAdminUser


# 分页类
class AdminOrderPagination(PageNumberPagination):
    page_size = 20  # 默认每页20条
    page_size_query_param = "page_size"  # 前端可通过 ?page_size=50 调整
    max_page_size = 100  # 每页最多100条


class AdminOrderListView(ListAPIView):
    """
    后台订单列表接口（分页）
    - 仅允许超级管理员 / is_staff 用户访问
    - 返回格式：{ count, next, previous, results }
    - 可支持 ?page=1&page_size=20 查询分页
    """

    permission_classes = [CustomIsAdminUser]
    queryset = Order.objects.select_related("user").all()
    serializer_class = AdminOrderListSerializer
    pagination_class = AdminOrderPagination

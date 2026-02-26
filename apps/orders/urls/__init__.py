# apps/orders/urls/__init__.py
from django.urls import path, include

urlpatterns = [
    # 前台订单接口
    path("frontend/orders/", include("apps.orders.urls.frontend")),
    # 后台订单接口
    path("admin/", include("apps.orders.urls.admin")),
]

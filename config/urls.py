# config/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from core.views import health

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    # ===== 健康检查（监控专用）=====
    path("health/", health),
    # ===== JWT =====
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # ===== API =====
    path("api/users/", include("apps.users.urls")),  # 用户/管理员
    path("api/", include("apps.inventory.urls")),  # 库存
    path("api/", include("apps.reviews.urls")),  # 评论
    path("api/", include("apps.orders.urls")),  # 订单
    path("api/", include("apps.products.urls")),  # 产品
    path("api/", include("apps.content.urls.frontend")),  # 页面内容
    path("api/admin/", include("apps.content.urls.admin")),  # 页面内容
    path("api/", include("apps.system.urls.company")),  # 公司介绍
]

# 只有 DEBUG=True 时才允许直接访问 media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

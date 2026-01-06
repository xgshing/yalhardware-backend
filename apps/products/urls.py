# products/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views_admin import ProductImageUploadView

# ===== 前台 views（只读） =====
from .views import (
    ProductListAPIView,
    ProductDetailAPIView,
    CategoryTreeAPIView,    # 分类树
)

# ===== 后台 views（管理） =====
from .views_admin import (
    AdminProductViewSet,
    ProductCategoryViewSet,
)


# =============================
# 后台 Router（统一 /admin/）
# =============================
admin_router = DefaultRouter()
admin_router.register(
    r'products',
    AdminProductViewSet,
    basename='admin-products'
)
admin_router.register(
    r'categories',
    ProductCategoryViewSet,
    basename='admin-categories'
)

# =============================
# URL patterns
# =============================
urlpatterns = [

    # ---------- 前台公共接口 ----------
    path(
        'products/',
        ProductListAPIView.as_view(),
        name='product-list'
    ),
    path(
        'products/<int:pk>/',
        ProductDetailAPIView.as_view(),
        name='product-detail'
    ),
    path(
        'categories/',
        CategoryTreeAPIView.as_view(),
        name='category-tree'
    ),
    # ---------- 后台管理接口 ----------
    path(
        'admin/',
        include(admin_router.urls)
    ),
    # ---------- Cloudinary 上传图片接口 ----------
    path("admin/upload/image/", ProductImageUploadView.as_view()),
]


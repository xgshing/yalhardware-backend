#处理请求结构（FormData / JSON / Files）
# apps/products/views.py

from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny

from .models import Product

from .serializers.product_detail import ProductDetailSerializer
from .serializers.product_create import ProductCreateSerializer
from .serializers.product_update import ProductUpdateSerializer

from .models import ProductCategory
from .serializers.category_tree import CategoryTreeSerializer

class ProductListAPIView(ListAPIView):
    """
    前台公共接口：产品列表
    GET /api/products/
    """
    permission_classes = [AllowAny]
    serializer_class = ProductDetailSerializer
    def get_queryset(self):
        return (
            Product.objects
            .filter(is_active=True)
            .select_related('category')
            .prefetch_related('detail_images', 'variants')
            .order_by('-created_at')[:20]
        )


class ProductDetailAPIView(RetrieveAPIView):
    """
    前台公共接口：产品详情
    GET /api/products/<id>/
    """
    permission_classes = [AllowAny]
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductDetailSerializer


class ProductCreateAPIView(CreateAPIView):
    """
    后台管理接口：创建产品
    POST /api/admin/products/
    """
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer


class ProductUpdateAPIView(UpdateAPIView):
    """
    后台管理接口：更新产品
    PUT / PATCH /api/admin/products/<id>/
    """
    queryset = Product.objects.all()
    serializer_class = ProductUpdateSerializer


class CategoryTreeAPIView(ListAPIView):
    """
    前台公共接口：分类树
    GET /api/categories/
    """
    permission_classes = [AllowAny]
    serializer_class = CategoryTreeSerializer

    def get_queryset(self):
        # 只返回「父分类」（parent = None）
        return ProductCategory.objects.filter(parent__isnull=True)

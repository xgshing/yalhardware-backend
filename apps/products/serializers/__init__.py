# 所有外部 import 都从这里进
# serializers/__init__.py
from .category import ProductCategorySerializer
from .image import ProductImageSerializer
from .variant import ProductVariantSerializer

from .product_create import ProductCreateSerializer
from .product_update import ProductUpdateSerializer
from .product_detail import ProductDetailSerializer

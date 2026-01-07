# apps/products/serializers/product_detail.py
from rest_framework import serializers
from ..models import Product
from .category import ProductCategorySerializer
from .image import ProductImageSerializer
from .variant import ProductVariantSerializer

class ProductDetailSerializer(serializers.ModelSerializer):
    # 👉 用于展示
    category = ProductCategorySerializer(read_only=True)
    # 👉 用于编辑（关键）
    category_id = serializers.PrimaryKeyRelatedField(
        source='category',
        queryset=Product._meta.get_field('category').remote_field.model.objects.all(),
        write_only=True,
        required=False,
        allow_null=True
    )

    detail_images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    # cover_url 用于展示 Cloudinary URL
    cover_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            # 分类
            'category',     # 只读（回显）
            'category_id',  # 可写（提交）
            # 基础信息
            'price',
            'description',
            'specifications',
            # 状态
            'is_active',
            'is_featured',
            'featured_order',
            # 图片
            'cover',
            'cover_url',
            'detail_images',
            # 款式
            'variants',
            # 时间
            'created_at',
        ]

    def get_cover_url(self, obj):
        """
        返回完整 URL，支持本地和 Cloudinary
        """
        if not obj.cover:
            return None

        try:
            # 本地 FileSystemStorage
            return obj.cover.url
        except Exception:
            # Cloudinary / URL 字符串兜底
            return str(obj.cover)

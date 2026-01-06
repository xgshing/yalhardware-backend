# apps/products/serializers/product_create.py
from rest_framework import serializers
from ..models import Product, ProductImage, ProductVariant, ProductCategory
from .product_base import BaseProductWriteSerializer

class ProductCreateSerializer(BaseProductWriteSerializer):
    """
    后台创建产品用序列化器
    - 包含查重逻辑
    - 处理分类
    """
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductCategory.objects.all(),
        write_only=True,
        source='category',
        allow_null=True,
        required=False
    )

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'category_id',
            'price',
            'description',
            'specifications',
            'is_active',
            'is_featured',
            'featured_order',
            'uploaded_images',
            'uploaded_variants',
        ]

    def validate(self, attrs):
        name = attrs.get('name')
        category = attrs.get('category')
        if Product.objects.filter(name=name, category=category).exists():
            raise serializers.ValidationError(
                {'name': '该分类下已存在同名产品'}
            )
        return attrs

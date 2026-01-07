# apps/products/serializers/product_create.py
from rest_framework import serializers
from ..models import Product, ProductImage, ProductVariant, ProductCategory
from .product_base import BaseProductWriteSerializer

class ProductCreateSerializer(BaseProductWriteSerializer):
    # 保留上传 variants 的 JSONField
    uploaded_variants = serializers.JSONField(
        write_only=True,
        required=False
    )

    # 写：接收分类 ID
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
            'cover',
            'featured_order',
            'uploaded_images',
            'uploaded_variants',
        ]

    def validate(self, attrs):
        """
        同分类下，产品名不能重复
        """
        name = attrs.get('name')
        category = attrs.get('category')

        if Product.objects.filter(
            name=name,
            category=category
        ).exists():
            raise serializers.ValidationError(
                {'name': '该分类下已存在同名产品'}
            )
        return attrs

    def create(self, validated_data):
        # ❌ 不处理任何图片
        validated_data.pop('uploaded_images', None)
        validated_data.pop('uploaded_variants', None)
        validated_data.pop('cover', None)

        # 创建 Product
        product = Product.objects.create(**validated_data)

        return product

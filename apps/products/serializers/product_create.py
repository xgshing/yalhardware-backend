 # 创建校验
# serializers/product_create.py
from ..models import Product, ProductImage, ProductVariant
from .product_base import BaseProductWriteSerializer

from rest_framework import serializers
from ..models import Product
from ..models import ProductCategory

class ProductCreateSerializer(BaseProductWriteSerializer):
    uploaded_variants = serializers.JSONField(
        write_only=True,
        required=False
    )

    def create(self, validated_data):
        images = validated_data.pop('uploaded_images', [])
        variants_data = validated_data.pop('uploaded_variants', [])

        product = Product.objects.create(**validated_data)

        for img in images:
            ProductImage.objects.create(product=product, image=img)

        for variant in variants_data:
            ProductVariant.objects.create(product=product, **variant)

        return product


    """
    后台：创建产品用
    - 包含查重逻辑
    """

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

# apps/products/serializers/product_create.py
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
        # 提取前端上传的图片和 variants
        images = validated_data.pop('uploaded_images', [])
        variants_data = validated_data.pop('uploaded_variants', [])

        # 上传 cover 到 Cloudinary（或本地）
        cover_file = validated_data.pop('cover', None)
        if cover_file:
            validated_data['cover'] = self._upload(cover_file, folder="products/covers")

        # 创建 Product
        product = Product.objects.create(**validated_data)

        # 上传 detail_images
        for img in images:
            file_or_url = self._upload(img, folder="products/details")
            ProductImage.objects.create(product=product, image=file_or_url)

        # 上传 variants
        for variant in variants_data:
            # 取出上传的文件
            image = variant.pop('style_image', None)
            if image:
                variant['style_image'] = self._upload(image, folder="products/variants")

            # 只保留 ProductVariant 模型字段，过滤掉 uid, hasImage, imageUrl, remove_image
            allowed_fields = {f.name for f in ProductVariant._meta.fields if f.name not in ['id', 'product']}
            clean_variant = {k: v for k, v in variant.items() if k in allowed_fields}

            ProductVariant.objects.create(product=product, **clean_variant)

        return product

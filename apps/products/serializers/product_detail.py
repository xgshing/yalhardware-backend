# apps/products/serializers/product_detail.py
from rest_framework import serializers
from ..models import Product
from .category import ProductCategorySerializer
from .image import ProductImageSerializer
from .variant import ProductVariantSerializer
from django.conf import settings

class ProductDetailSerializer(serializers.ModelSerializer):
    # 分类展示
    category = ProductCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        source='category',
        queryset=Product._meta.get_field('category').remote_field.model.objects.all(),
        write_only=True,
        required=False,
        allow_null=True
    )

    # 详情图、variants
    detail_images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    # 主图 cover
    cover = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'category',
            'category_id',
            'price',
            'description',
            'specifications',
            'is_active',
            'is_featured',
            'featured_order',
            'cover',
            'detail_images',
            'variants',
            'created_at',
        ]

    def get_cover(self, obj):
        if not obj.cover:
            return None
        request = self.context.get('request')
        # Cloudinary URL
        if obj.cover.startswith('http'):
            return obj.cover
        # 本地 media
        if request:
            return request.build_absolute_uri(settings.MEDIA_URL + obj.cover.lstrip('/'))
        return settings.MEDIA_URL + obj.cover.lstrip('/')

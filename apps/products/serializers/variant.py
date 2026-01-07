# apps/products/serializers/variant.py
from rest_framework import serializers
from ..models import ProductVariant

class ProductVariantSerializer(serializers.ModelSerializer):
    style_image = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = [
            'id',
            'style_name',
            'spec',
            'stock',
            'style_image',
        ]

    def get_style_image(self, obj):
        """
        返回可访问的款式图片 URL
        """
        if not obj.style_image:
            return None

        try:
            return obj.style_image.url
        except Exception:
            return str(obj.style_image)

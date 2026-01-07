# apps/products/serializers/image.py
from rest_framework import serializers
from ..models import ProductImage, ProductVariant

class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'image']

    def get_image(self, obj):
        """
        返回可访问的图片 URL
        """
        if not obj.image:
            return None

        try:
            return obj.image.url
        except Exception:
            return str(obj.image)


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
        request = self.context.get('request')
        if obj.style_image:
            return request.build_absolute_uri(obj.style_image.url)
        return None

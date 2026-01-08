# apps/products/serializers/variant.py
from rest_framework import serializers
from ..models import ProductVariant
from django.conf import settings

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
        if not obj.style_image:
            return None
        request = self.context.get('request')
        # Cloudinary URL
        if obj.style_image.startswith('http'):
            return obj.style_image
        # 本地 media
        if request:
            return request.build_absolute_uri(settings.MEDIA_URL + obj.style_image.lstrip('/'))
        return settings.MEDIA_URL + obj.style_image.lstrip('/')


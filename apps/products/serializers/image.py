# apps/products/serializers/image.py
from rest_framework import serializers
from ..models import ProductImage
from django.conf import settings

class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'image']

    def get_image(self, obj):
        if not obj.image:
            return None
        request = self.context.get('request')
        # Cloudinary URL
        if obj.image.startswith('http'):
            return obj.image
        # 本地 media
        if request:
            return request.build_absolute_uri(settings.MEDIA_URL + obj.image.lstrip('/'))
        return settings.MEDIA_URL + obj.image.lstrip('/')



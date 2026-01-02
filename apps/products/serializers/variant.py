# serializers/variant.py
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
        if obj.style_image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.style_image.url)
        return None

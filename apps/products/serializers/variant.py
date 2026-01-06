# apps/products/serializers/variant.py
from rest_framework import serializers
from ..models import ProductVariant


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = [
            'id',
            'style_name',
            'spec',
            'stock',
            'style_image',
        ]

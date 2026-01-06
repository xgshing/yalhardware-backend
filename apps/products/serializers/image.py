# 产品图片“展示用”
# apps/products/serializers/image.py
from rest_framework import serializers
from ..models import ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']
# Product 公共字段。用来消除 Create / Update 的重复定义
# serializers/product_base.py
from rest_framework import serializers
from ..models import Product


class BaseProductWriteSerializer(serializers.ModelSerializer):
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    # 🔥 关键：用 JSONField 接字符串
    uploaded_variants = serializers.JSONField(
        write_only=True,
        required=False
    )

    class Meta:
        model = Product
        fields = [
            'name',
            'category',
            'price',
            'description',
            'specifications',
            'is_active',
            'cover',
            'is_featured',
            'uploaded_images',
            'uploaded_variants',
        ]

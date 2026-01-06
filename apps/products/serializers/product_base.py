# apps/products/serializers/product_base.py
from rest_framework import serializers
from ..models import Product

class BaseProductWriteSerializer(serializers.ModelSerializer):
    """
    公共字段，用于 Create / Update，处理文件上传
    """
    uploaded_images = serializers.ListField(
        child=serializers.FileField(),  # ⚠ FileField 支持前端上传文件
        write_only=True,
        required=False
    )

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
            'is_featured',
            'uploaded_images',
            'uploaded_variants',
        ]

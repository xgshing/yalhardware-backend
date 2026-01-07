# apps/products/serializers/product_base.py
from rest_framework import serializers
from django.conf import settings
from ..models import Product, ProductVariant, ProductImage
from core.cloudinary import upload_image


class BaseProductWriteSerializer(serializers.ModelSerializer):
    cover = serializers.ImageField(
        required=False,
        allow_null=True
    )
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        allow_null=True,
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
            'cover',
            'is_featured',
        ]



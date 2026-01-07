# apps/products/serializers/product_update.py
from ..models import ProductImage, ProductVariant
from .product_base import BaseProductWriteSerializer


def update(self, instance, validated_data):
        # 🚫 防止字符串覆盖 ImageField
        cover = validated_data.get("cover")
        if isinstance(cover, str):
            validated_data.pop("cover")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
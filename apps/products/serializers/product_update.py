# apps/products/serializers/product_update.py
from ..models import ProductImage, ProductVariant
from .product_base import BaseProductWriteSerializer


class ProductUpdateSerializer(BaseProductWriteSerializer):
    def update(self, instance, validated_data):
        # 只更新 Product 本身
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

# apps/products/serializers/category.py
from rest_framework import serializers
from ..models import ProductCategory


class ProductCategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'parent', 'children']

    def get_children(self, obj):
        return ProductCategorySerializer(
            obj.children.all(),
            many=True
        ).data

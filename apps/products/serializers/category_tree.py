# apps/products/serializers/category_tree.py
from rest_framework import serializers
from ..models import ProductCategory


class CategoryTreeSerializer(serializers.ModelSerializer):
    """
    前台分类树序列化器（只读）
    - 只返回 id / name / children
    """
    children = serializers.SerializerMethodField()

    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'children']

    def get_children(self, obj):
        children_qs = obj.children.all()
        return CategoryTreeSerializer(children_qs, many=True).data
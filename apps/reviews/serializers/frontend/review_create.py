# 创建评论
# apps/reviews/serializers/frontend/review_create.py
from rest_framework import serializers
from apps.reviews.models import Review
from apps.orders.models import OrderItem


class ReviewCreateSerializer(serializers.Serializer):
    order_item_id = serializers.IntegerField()
    rating = serializers.IntegerField(min_value=1, max_value=5)
    content = serializers.CharField()
    images = serializers.ListField(child=serializers.ImageField(), required=False)

    def validate_order_item_id(self, value):
        user = self.context["request"].user
        try:
            item = OrderItem.objects.select_related("order").get(id=value)
        except OrderItem.DoesNotExist:
            raise serializers.ValidationError("订单商品不存在")

        if item.order.user != user:
            raise serializers.ValidationError("无权限评价该订单")
        if item.order.status != item.order.Status.COMPLETED:
            raise serializers.ValidationError("订单未完成，无法评价")
        if hasattr(item, "review"):
            raise serializers.ValidationError("该商品已评价")

        return value

    def create(self, validated_data):
        order_item = OrderItem.objects.get(id=validated_data["order_item_id"])
        return Review.objects.create(
            order_item=order_item,
            user=self.context["request"].user,
            rating=validated_data["rating"],
            content=validated_data["content"],
            images=validated_data.get("images", []),
        )

# 订单商品行
# apps/orders/serializers/frontend/order_item.py

from django.conf import settings
from rest_framework import serializers

from apps.orders.models import OrderItem
from apps.reviews.models import Review
from apps.reviews.serializers.frontend.review_read import ReviewReadSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    review = serializers.SerializerMethodField()
    can_review = serializers.SerializerMethodField()
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product_id",
            "product_title",
            "sku_title",
            "price",
            "quantity",
            "review",
            "can_review",
            "product_image",
        ]

    # ===============================
    # 商品图片（生产级 URL 处理）
    # ===============================
    def get_product_image(self, obj):
        """
        OrderItem.product_image 是 URLField（字符串）
        可能是：
        - Cloudinary 返回的完整 URL
        - 本地 FileSystemStorage 的相对路径（products/variants/xxx.jpg）

        返回：
        - 永远是【前端可直接访问的完整 URL】
        """
        image = obj.product_image
        if not image:
            return None

        # 1️⃣ 已经是完整 URL（Cloudinary / 外链）
        if image.startswith("http://") or image.startswith("https://"):
            return image

        # 2️⃣ 本地存储的相对路径 → 拼 MEDIA_URL
        media_url = settings.MEDIA_URL.rstrip("/")
        path = f"{media_url}/{image}".replace("//", "/")

        # 3️⃣ 有 request（推荐，自动适配域名 / https）
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(path)

        # 4️⃣ fallback（极端情况）
        return path

    # ===============================
    # 评价信息
    # ===============================
    def get_review(self, obj):
        """
        已评价：返回完整评论结构
        未评价：返回 None
        """
        try:
            review = obj.review
        except Review.DoesNotExist:
            return None

        return ReviewReadSerializer(review).data

    # ===============================
    # 是否可评价
    # ===============================
    def get_can_review(self, obj):
        request = self.context.get("request")

        # 1. 必须是当前用户的订单
        if obj.order.user != request.user:
            return False

        # 2. 必须是已完成订单
        if obj.order.status != obj.order.Status.COMPLETED:
            return False

        # 3. 必须未评价
        if hasattr(obj, "review"):
            return False

        return True

# 订单列表专用
# apps/orders/serializers/order_list.py
from django.conf import settings
from rest_framework import serializers
from apps.orders.models import Order
from apps.orders.services.order_actions import get_available_actions


class OrderItemListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    product_title = serializers.CharField()
    sku_title = serializers.CharField(allow_blank=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField()
    subtotal = serializers.SerializerMethodField()
    product_image = serializers.SerializerMethodField()

    def get_subtotal(self, obj):
        return float(obj.price * obj.quantity)

    def get_product_image(self, obj):
        """
        订单列表商品图（生产级）
        """
        image = obj.product_image
        if not image:
            return None

        # Cloudinary / 外链
        if image.startswith("http://") or image.startswith("https://"):
            return image

        # 本地相对路径
        media_url = settings.MEDIA_URL.rstrip("/")
        path = f"{media_url}/{image}".replace("//", "/")

        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(path)

        return path


class OrderListSerializer(serializers.ModelSerializer):
    status = serializers.CharField()
    status_label = serializers.CharField(source="get_status_display")
    total_amount = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()
    available_actions = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "order_no",
            "status",
            "status_label",
            "created_at",
            "total_amount",
            "items",
            "available_actions",
        ]

    def get_total_amount(self, obj):
        return float(obj.total_amount)

    def get_items(self, obj):
        items = obj.items.all()
        return OrderItemListSerializer(
            items,
            many=True,
            context=self.context,
        ).data

    def get_available_actions(self, obj):
        return get_available_actions(obj)

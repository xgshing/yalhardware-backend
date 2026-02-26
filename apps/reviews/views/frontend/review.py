# 评论列表 / 创建接口
# apps/reviews/views/frontend/review.py
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.reviews.models import Review
from apps.reviews.serializers.frontend.review_read import ReviewReadSerializer
from apps.reviews.serializers.frontend.review_create import ReviewCreateSerializer


class ReviewViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        支持按 product_id 或 order_item_id 查询
        """
        qs = (
            Review.objects.select_related("order_item", "order_item__product", "user")
            .prefetch_related("reply")
            .order_by("-created_at")
        )

        product_id = self.request.query_params.get("product_id")
        order_item_id = self.request.query_params.get("order_item_id")

        if product_id:
            # 使用 order_item 的 product_id 外键
            qs = qs.filter(order_item__product_id=product_id)
        elif order_item_id:
            qs = qs.filter(order_item_id=order_item_id)

        return qs

    def get_serializer_class(self):
        if self.action == "create":
            return ReviewCreateSerializer
        return ReviewReadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        review = serializer.save()
        return Response(ReviewReadSerializer(review).data)

    def list(self, request, *args, **kwargs):
        """
        重写 list，使按 order_item_id 查询时只返回单条评价（如果存在）
        """
        queryset = self.filter_queryset(self.get_queryset())

        order_item_id = request.query_params.get("order_item_id")
        if order_item_id:
            review = queryset.first()
            if review:
                # 兼容新老订单显示商品名称
                data = ReviewReadSerializer(review).data
                if hasattr(review.order_item, "product") and review.order_item.product:
                    data["product_name"] = review.order_item.product.name
                else:
                    data["product_name"] = review.order_item.product_title
                return Response(data)
            else:
                return Response(None, status=status.HTTP_200_OK)

        # product_id 查询保持列表
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ReviewReadSerializer(page, many=True)
            # 兼容 product 外键
            for i, review in enumerate(page):
                if hasattr(review.order_item, "product") and review.order_item.product:
                    serializer.data[i]["product_name"] = review.order_item.product.name
                else:
                    serializer.data[i]["product_name"] = review.order_item.product_title
            return self.get_paginated_response(serializer.data)

        serializer = ReviewReadSerializer(queryset, many=True)
        # 兼容 product 外键
        for i, review in enumerate(queryset):
            if review.order_item.product:
                serializer.data[i]["product_name"] = review.order_item.product.name
            else:
                serializer.data[i]["product_name"] = review.order_item.product_title

        return Response(serializer.data)

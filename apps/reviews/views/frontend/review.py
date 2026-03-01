# 评论列表 / 创建接口
# apps/reviews/views/frontend/review.py
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.reviews.models import Review
from apps.reviews.serializers.frontend.review_read import ReviewReadSerializer
from apps.reviews.serializers.frontend.review_create import ReviewCreateSerializer
from apps.reviews.serializers.frontend.review_append import ReviewAppendSerializer


class ReviewViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """
    评论接口
    支持：
    - GET /reviews/ : 评论列表，可通过 query_params 过滤 product_id 或 order_item_id
    - POST /reviews/ : 创建评论
    - POST /reviews/append/ : 追加评论
    """

    # 默认 queryset
    queryset = (
        Review.objects.select_related("order_item", "order_item__product", "user")
        .prefetch_related("reply")
        .order_by("-created_at")
    )

    def get_queryset(self):
        """
        支持按 product_id 或 order_item_id 过滤
        """
        queryset = super().get_queryset()
        request = self.request

        # 获取 query 参数
        order_item_id = request.query_params.get("order_item_id")
        product_id = request.query_params.get("product_id")

        if order_item_id:
            queryset = queryset.filter(order_item_id=order_item_id)

        if product_id:
            queryset = queryset.filter(order_item__product_id=product_id)

        return queryset

    def get_serializer_class(self):
        if self.action == "create":
            return ReviewCreateSerializer
        return ReviewReadSerializer

    def create(self, request, *args, **kwargs):
        """
        创建评论
        """
        serializer = ReviewCreateSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        review = serializer.save()
        return Response(
            ReviewReadSerializer(review).data, status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def append(self, request):
        """
        追加评论
        """
        serializer = ReviewAppendSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        review = serializer.save()
        return Response(ReviewReadSerializer(review).data)

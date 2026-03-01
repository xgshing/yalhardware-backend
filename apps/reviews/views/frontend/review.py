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
    queryset = (
        Review.objects.select_related("order_item", "order_item__product", "user")
        .prefetch_related("reply")
        .order_by("-created_at")
    )

    def get_serializer_class(self):
        if self.action == "create":
            return ReviewCreateSerializer
        return ReviewReadSerializer

    def create(self, request, *args, **kwargs):
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
        serializer = ReviewAppendSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        review = serializer.save()
        return Response(ReviewReadSerializer(review).data)

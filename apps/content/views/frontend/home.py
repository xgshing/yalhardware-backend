# 前台 View（一个接口返回整个首页）
# apps/content/views/frontend/home.py
from rest_framework.views import APIView
from rest_framework.response import Response

from ...models.home import HomeBanner, HomeFeature, HomeStory
from ...serializers.frontend.home import (
    HomeBannerSerializer,
    HomeFeatureSerializer,
    HomeStorySerializer,
)


class HomeAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        banners = (
            HomeBanner.objects
            .filter(is_active=True)
            .prefetch_related('images')
            .order_by('-created_at')[:10]
        )

        features = (
            HomeFeature.objects
            .filter(is_active=True)
            .prefetch_related('images')
            .order_by('-created_at')[:10]
        )

        stories = (
            HomeStory.objects
            .filter(is_active=True)
            .prefetch_related('images')
            .order_by('-created_at')[:10]
        )

        return Response({
            'banners': HomeBannerSerializer(banners, many=True, context={'request': request}).data,
            'features': HomeFeatureSerializer(features, many=True, context={'request': request}).data,
            'stories': HomeStorySerializer(stories, many=True, context={'request': request}).data,
        })
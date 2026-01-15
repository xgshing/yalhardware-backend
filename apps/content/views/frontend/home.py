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
        return Response({
            'banners': HomeBannerSerializer(
                HomeBanner.objects.filter(is_active=True),
                many=True,
                context={'request': request},
            ).data,
            'features': HomeFeatureSerializer(
                HomeFeature.objects.filter(is_active=True),
                many=True,
                context={'request': request},
            ).data,
            'stories': HomeStorySerializer(
                HomeStory.objects.filter(is_active=True),
                many=True,
                context={'request': request},
            ).data,
        })
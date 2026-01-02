# 删除单张图片
# apps/content/views/admin/home_images.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser

from ...models.home import HomeBannerImage, HomeFeatureImage, HomeStoryImage
from ...serializers.admin.image import (
    HomeBannerImageSerializer,
    HomeFeatureImageSerializer,
    HomeStoryImageSerializer,
)


# ---------------- Banner Image ----------------
class AdminHomeBannerImageViewSet(ModelViewSet):
    queryset = HomeBannerImage.objects.all()
    serializer_class = HomeBannerImageSerializer
    permission_classes = [IsAdminUser]


# ---------------- Feature Image ----------------
class AdminHomeFeatureImageViewSet(ModelViewSet):
    queryset = HomeFeatureImage.objects.all()
    serializer_class = HomeFeatureImageSerializer
    permission_classes = [IsAdminUser]


# ---------------- Story Image ----------------
class AdminHomeStoryImageViewSet(ModelViewSet):
    queryset = HomeStoryImage.objects.all()
    serializer_class = HomeStoryImageSerializer
    permission_classes = [IsAdminUser]

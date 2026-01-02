# 后台 CRUD ViewSet
# apps/content/views/admin/home.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework import  permissions

from ...models.home import HomeBanner, HomeBannerImage, HomeFeature, HomeFeatureImage, HomeStory, HomeStoryImage
from ...serializers.admin.home import (
    AdminHomeBannerSerializer,
    AdminHomeFeatureSerializer,
    AdminHomeStorySerializer,
)
from .mixins.image_actions import MultiImageActionsMixin


class AdminHomeBannerViewSet(
    MultiImageActionsMixin,
    ModelViewSet
):
    queryset = HomeBanner.objects.all()
    serializer_class = AdminHomeBannerSerializer
    permission_classes = [permissions.AllowAny]

    image_model = HomeBannerImage
    image_fk_field = 'banner'



class AdminHomeFeatureViewSet(
    MultiImageActionsMixin,
    ModelViewSet
):
    queryset = HomeFeature.objects.all()
    serializer_class = AdminHomeFeatureSerializer
    permission_classes = [permissions.AllowAny]

    image_model = HomeFeatureImage
    image_fk_field = 'feature'



class AdminHomeStoryViewSet(
    MultiImageActionsMixin,
    ModelViewSet
):
    queryset = HomeStory.objects.all()
    serializer_class = AdminHomeStorySerializer
    permission_classes = [permissions.AllowAny]

    image_model = HomeStoryImage
    image_fk_field = 'story'

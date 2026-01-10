# apps/content/views/admin/home.py
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from ...models.home import (
    HomeBanner, HomeBannerImage,
    HomeFeature, HomeFeatureImage,
    HomeStory, HomeStoryImage,
)
from ...serializers.admin.home import (
    AdminHomeBannerSerializer,
    AdminHomeFeatureSerializer,
    AdminHomeStorySerializer,
)
from .mixins.image_actions import MultiImageActionsMixin


class BaseAdminHomeViewSet(MultiImageActionsMixin, ModelViewSet):
    """
    后台 Home CRUD + 多图操作
    子类必须指定：
      - queryset
      - serializer_class
      - image_model
      - image_fk_field
      - file_field（可选，默认 'image'）
      - cloud_folder（可选）
    """
    permission_classes = [permissions.AllowAny]


class AdminHomeBannerViewSet(BaseAdminHomeViewSet):
    queryset = HomeBanner.objects.all()
    serializer_class = AdminHomeBannerSerializer
    image_model = HomeBannerImage
    image_fk_field = 'banner'
    file_field = 'image'
    cloud_folder = 'home/banners'


class AdminHomeFeatureViewSet(BaseAdminHomeViewSet):
    queryset = HomeFeature.objects.all()
    serializer_class = AdminHomeFeatureSerializer
    image_model = HomeFeatureImage
    image_fk_field = 'feature'
    file_field = 'image'
    cloud_folder = 'home/features'


class AdminHomeStoryViewSet(BaseAdminHomeViewSet):
    queryset = HomeStory.objects.all()
    serializer_class = AdminHomeStorySerializer
    image_model = HomeStoryImage
    image_fk_field = 'story'
    file_field = 'image'
    cloud_folder = 'home/stories'

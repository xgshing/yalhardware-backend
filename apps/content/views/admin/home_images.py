# 删除单张图片
# apps/content/views/admin/home_images.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from django.conf import settings

from ...models.home import HomeBannerImage, HomeFeatureImage, HomeStoryImage
from ...serializers.admin.image import (
    HomeBannerImageSerializer,
    HomeFeatureImageSerializer,
    HomeStoryImageSerializer,
)
from .mixins.image_actions import MultiImageActionsMixin
from core.upload import upload_image

class BaseAdminImageViewSet(ModelViewSet, MultiImageActionsMixin):
    """
    通用图片上传逻辑：
    - 本地 SQLite 存本地
    - 生产 PostgreSQL 上传 Cloudinary
    """
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        file_field_name = getattr(self, 'file_field_name', 'image')
        file = self.request.FILES.get(file_field_name)

        if file:
            url = upload_image(file, folder=self.cloud_folder)
            serializer.save(**{file_field_name: url})
        else:
            serializer.save()


# ---------------- Banner Image ----------------
class AdminHomeBannerImageViewSet(BaseAdminImageViewSet):
    queryset = HomeBannerImage.objects.all()
    serializer_class = HomeBannerImageSerializer
    permission_classes = [IsAdminUser]
    file_field_name = 'image'
    cloud_folder = 'home/banners'


# ---------------- Feature Image ----------------
class AdminHomeFeatureImageViewSet(BaseAdminImageViewSet):
    queryset = HomeFeatureImage.objects.all()
    serializer_class = HomeFeatureImageSerializer
    permission_classes = [IsAdminUser]
    file_field_name = 'image'
    cloud_folder = 'home/features'


# ---------------- Story Image ----------------
class AdminHomeStoryImageViewSet(BaseAdminImageViewSet):
    queryset = HomeStoryImage.objects.all()
    serializer_class = HomeStoryImageSerializer
    permission_classes = [IsAdminUser]
    file_field_name = 'image'
    cloud_folder = 'home/stories'
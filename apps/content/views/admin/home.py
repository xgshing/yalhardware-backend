# 后台 CRUD ViewSet
# apps/content/views/admin/home.py
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from django.conf import settings
from core.cloudinary import upload_image

from ...models.home import (
    HomeBanner,
    HomeBannerImage,
    HomeFeature,
    HomeFeatureImage,
    HomeStory,
    HomeStoryImage,
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
    - image_model: 对应图片模型
    - image_fk_field: 外键字段名
    - Cloudinary 上传逻辑统一处理
    """

    def perform_create(self, serializer):
        instance = serializer.save()

        uploaded_files = self.request.FILES.getlist('uploaded_images')
        for file in uploaded_files:
            if file:
                if settings.DATABASES['default']['ENGINE'].endswith('sqlite3'):
                    # 本地直接保存
                    self.image_model.objects.create(
                        **{self.image_fk_field: instance, self.file_field: file}
                    )
                else:
                    # 生产上传 Cloudinary
                    url = upload_image(file, folder=self.cloud_folder)
                    self.image_model.objects.create(
                        **{self.image_fk_field: instance, self.file_field: url}
                    )

    @property
    def file_field(self):
        """
        子类必须覆盖 image_model 中的图片字段名
        """
        if hasattr(self, '_file_field'):
            return self._file_field
        return 'image'

    @property
    def cloud_folder(self):
        """
        子类可覆盖对应 Cloudinary 文件夹
        """
        return 'home'


class AdminHomeBannerViewSet(BaseAdminHomeViewSet):
    queryset = HomeBanner.objects.all()
    serializer_class = AdminHomeBannerSerializer
    permission_classes = [permissions.AllowAny]

    image_model = HomeBannerImage
    image_fk_field = 'banner'
    _file_field = 'image'
    cloud_folder = 'home/banners'


class AdminHomeFeatureViewSet(BaseAdminHomeViewSet):
    queryset = HomeFeature.objects.all()
    serializer_class = AdminHomeFeatureSerializer
    permission_classes = [permissions.AllowAny]

    image_model = HomeFeatureImage
    image_fk_field = 'feature'
    _file_field = 'icon'
    cloud_folder = 'home/features'


class AdminHomeStoryViewSet(BaseAdminHomeViewSet):
    queryset = HomeStory.objects.all()
    serializer_class = AdminHomeStorySerializer
    permission_classes = [permissions.AllowAny]

    image_model = HomeStoryImage
    image_fk_field = 'story'
    _file_field = 'image'
    cloud_folder = 'home/stories'

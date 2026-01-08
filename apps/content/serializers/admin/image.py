# 多图片 Serializer（通用）
# apps/content/serializers/admin/image.py
from rest_framework import serializers
from django.conf import settings
from core.cloudinary import upload_image
from ...models.home import HomeBannerImage, HomeFeatureImage, HomeStoryImage


class ImageBaseSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)

    def get_image_url(self, obj):
        request = self.context.get('request')
        file_field = getattr(obj, 'image', None) or getattr(obj, 'icon', None)
        if not file_field:
            return ''
        # 字符串（Cloudinary URL）
        if isinstance(file_field, str):
            return file_field
        # FileField
        try:
            return request.build_absolute_uri(file_field.url)
        except Exception:
            return str(file_field)  # 兜底

    def _upload(self, file, folder):
        from django.conf import settings
        from core.cloudinary import upload_image
        if settings.DATABASES['default']['ENGINE'].endswith('sqlite3'):
            return file
        return upload_image(file, folder)


# ================= Banner Image =================
class HomeBannerImageSerializer(ImageBaseSerializer):
    class Meta:
        model = HomeBannerImage
        fields = ['id', 'image', 'image_url', 'order']


# ================= Feature Image =================
class HomeFeatureImageSerializer(ImageBaseSerializer):
    class Meta:
        model = HomeFeatureImage
        fields = ['id', 'icon', 'image_url', 'order']


# ================= Story Image =================
class HomeStoryImageSerializer(ImageBaseSerializer):
    class Meta:
        model = HomeStoryImage
        fields = ['id', 'image', 'image_url', 'order']

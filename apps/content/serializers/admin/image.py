# apps/content/serializers/admin/image.py
from rest_framework import serializers
from django.conf import settings
from ...models.home import HomeBannerImage, HomeFeatureImage, HomeStoryImage


def resolve_image_url(file_field, request=None):
    if not file_field:
        return ''

    # ================= 关键修复 =================
    # ImageField 里存的是 Cloudinary URL（字符串）
    raw_value = str(file_field)
    if raw_value.startswith('http://') or raw_value.startswith('https://'):
        return raw_value
    # ============================================

    # ===== 正常本地 ImageField =====
    if hasattr(file_field, 'url'):
        try:
            if request:
                return request.build_absolute_uri(file_field.url)
            return file_field.url
        except Exception:
            pass

    # ===== Cloudinary 旧数据（public_id）=====
    cloud_name = getattr(settings, 'CLOUDINARY_CLOUD_NAME', None)
    if cloud_name:
        return f'https://res.cloudinary.com/{cloud_name}/image/upload/{raw_value}'

    return raw_value


class ImageBaseSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)

    def get_image_url(self, obj):
        request = self.context.get('request')
        file_field = getattr(obj, 'image', None)
        return resolve_image_url(file_field, request)


# ================= Banner Image =================
class HomeBannerImageSerializer(ImageBaseSerializer):
    class Meta:
        model = HomeBannerImage
        fields = ['id', 'image', 'image_url', 'order']


# ================= Feature Image =================
class HomeFeatureImageSerializer(ImageBaseSerializer):
    class Meta:
        model = HomeFeatureImage
        fields = ['id', 'image', 'image_url', 'order']


# ================= Story Image =================
class HomeStoryImageSerializer(ImageBaseSerializer):
    class Meta:
        model = HomeStoryImage
        fields = ['id', 'image', 'image_url', 'order']

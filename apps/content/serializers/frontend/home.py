# apps/content/serializers/frontend/home.py
from rest_framework import serializers
from django.conf import settings
from ...models.home import HomeBanner, HomeFeature, HomeStory


def resolve_image_url(file_field, request=None):
    """
    统一处理图片 URL：
    - 本地 ImageField（media）
    - Cloudinary 完整 URL（https://）
    - Cloudinary 旧数据（只存 public_id / 相对路径）
    """
    if not file_field:
        return ''

    # ===== FileField（本地开发）=====
    if hasattr(file_field, 'url'):
        try:
            if request:
                return request.build_absolute_uri(file_field.url)
            return file_field.url
        except Exception:
            pass

    # ===== 字符串（Cloudinary）=====
    url = str(file_field)

    # 已是完整 URL
    if url.startswith('http://') or url.startswith('https://'):
        return url

    # Cloudinary 旧数据：补全 secure_url
    cloud_name = getattr(settings, 'CLOUDINARY_CLOUD_NAME', None)
    if cloud_name:
        return f'https://res.cloudinary.com/{cloud_name}/image/upload/{url}'

    # 兜底
    return url


# ================= HomeBanner =================
class HomeBannerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = HomeBanner
        fields = [
            'id',
            'title',
            'description',
            'image',
            'button_text',
            'button_link',
        ]

    def get_image(self, obj):
        request = self.context.get('request')

        if not obj.images.exists():
            return ''

        img = obj.images.first()
        file_field = getattr(img, 'image', None)

        return resolve_image_url(file_field, request)


# ================= HomeFeature =================
class HomeFeatureSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()

    class Meta:
        model = HomeFeature
        fields = [
            'title',
            'description',
            'icon',
        ]

    def get_icon(self, obj):
        request = self.context.get('request')

        if not obj.images.exists():
            return ''

        img = obj.images.first()
        return resolve_image_url(img.image, request)


# ================= HomeStory =================
class HomeStorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = HomeStory
        fields = [
            'title',
            'description',
            'image',
        ]

    def get_image(self, obj):
        request = self.context.get('request')

        if not obj.images.exists():
            return ''

        img = obj.images.first()
        file_field = getattr(img, 'image', None)

        return resolve_image_url(file_field, request)


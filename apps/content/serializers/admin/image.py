# apps/content/serializers/admin/image.py
from rest_framework import serializers
from django.conf import settings
from ...models.home import HomeBannerImage, HomeFeatureImage, HomeStoryImage

class ImageURLMixin:
    def to_representation(self, instance):
        data = super().to_representation(instance)
        img = data.get('image')

        if not img:
            return data

        request = self.context.get('request')

        # 如果已经是完整 URL
        if img.startswith('http'):
            return data

        # 统一处理本地 media 文件
        if not img.startswith('/'):
            img = '/' + settings.MEDIA_URL.lstrip('/') + img.lstrip('/')
        elif not img.startswith(settings.MEDIA_URL):
            img = settings.MEDIA_URL.rstrip('/') + img

        # 补全域名
        if request:
            data['image'] = request.build_absolute_uri(img)
        else:
            data['image'] = img  # 如果没有 request，则返回 /media/... 也能在本地访问

        return data


# ================= Banner Image =================
class HomeBannerImageSerializer(ImageURLMixin, serializers.ModelSerializer):
    class Meta:
        model = HomeBannerImage
        fields = ['id', 'image', 'order']


class HomeFeatureImageSerializer(ImageURLMixin, serializers.ModelSerializer):
    class Meta:
        model = HomeFeatureImage
        fields = ['id', 'image', 'order']


class HomeStoryImageSerializer(ImageURLMixin, serializers.ModelSerializer):
    class Meta:
        model = HomeStoryImage
        fields = ['id', 'image', 'order']

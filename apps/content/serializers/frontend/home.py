# Serializer（前台展示用）
# apps/content/serializers/frontend/home.py
from rest_framework import serializers
from django.conf import settings
from core.cloudinary import upload_image
from ...models.home import HomeBanner, HomeFeature, HomeStory


class HomeBannerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = HomeBanner
        fields = [
            'id',
            'title',
            'description',  # 原 subtitle 改为 description 保持模型字段一致
            'image',
            'button_text',
            'button_link',
        ]

    def get_image(self, obj):
        request = self.context.get('request')
        if not obj.images.exists():
            return ''
        # 默认取第一张图作为展示
        img = obj.images.first()
        if hasattr(img, 'image') and img.image:
            return request.build_absolute_uri(img.image.url)
        return ''


class HomeFeatureSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()

    class Meta:
        model = HomeFeature
        fields = ['title', 'description', 'icon']

    def get_icon(self, obj):
        request = self.context.get('request')
        if not obj.images.exists():
            return ''
        # 默认取第一张图作为 icon
        icon_obj = obj.images.first()
        if hasattr(icon_obj, 'icon') and icon_obj.icon:
            return request.build_absolute_uri(icon_obj.icon.url)
        return ''


class HomeStorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = HomeStory
        fields = ['title', 'description', 'image']

    def get_image(self, obj):
        request = self.context.get('request')
        if not obj.images.exists():
            return ''
        img = obj.images.first()
        if hasattr(img, 'image') and img.image:
            return request.build_absolute_uri(img.image.url)
        return ''

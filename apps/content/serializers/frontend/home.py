# Serializer（前台展示用）
# apps/content/serializers/frontend/home.py
from rest_framework import serializers
from ...models.home import HomeBanner, HomeFeature, HomeStory


class HomeBannerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = HomeBanner
        fields = [
            'id',
            'title',
            'subtitle',
            'image',
            'button_text',
            'button_link',
        ]

    def get_image(self, obj):
        request = self.context.get('request')
        if not obj.image:
            return ''
        return request.build_absolute_uri(obj.image.url)


class HomeFeatureSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()

    class Meta:
        model = HomeFeature
        fields = ['title', 'description', 'icon']

    def get_icon(self, obj):
        if not obj.icon:
            return ''
        request = self.context.get('request')
        return request.build_absolute_uri(obj.icon.url)


class HomeStorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = HomeStory
        fields = ['title', 'description', 'image']

    def get_image(self, obj):
        request = self.context.get('request')
        if not obj.image:
            return ''
        return request.build_absolute_uri(obj.image.url)

# apps/content/serializers/frontend/home.py
from rest_framework import serializers
from ...models.home import HomeBanner, HomeFeature, HomeStory  # ✅ 导入模型

class HomeBannerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = HomeBanner
        fields = ['id', 'title', 'description', 'image', 'button_text', 'button_link']

    def get_image(self, obj):
        request = self.context.get('request')
        if not obj.images.exists():
            return ''
        img = obj.images.first()
        file_field = getattr(img, 'image', None)
        if not file_field:
            return ''
        if isinstance(file_field, str):
            return file_field
        if request:
            return request.build_absolute_uri(file_field.url)
        return file_field.url


class HomeFeatureSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()

    class Meta:
        model = HomeFeature
        fields = ['title', 'description', 'icon']

    def get_icon(self, obj):
        request = self.context.get('request')
        if not obj.images.exists():
            return ''
        icon_obj = obj.images.first()
        file_field = getattr(icon_obj, 'icon', None)
        if not file_field:
            return ''
        if isinstance(file_field, str):
            return file_field
        if request:
            return request.build_absolute_uri(file_field.url)
        return file_field.url


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
        file_field = getattr(img, 'image', None)
        if not file_field:
            return ''
        if isinstance(file_field, str):
            return file_field
        if request:
            return request.build_absolute_uri(file_field.url)
        return file_field.url

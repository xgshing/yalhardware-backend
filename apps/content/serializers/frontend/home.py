# apps/content/serializers/frontend/home.py
from rest_framework import serializers
from django.conf import settings
from ...models.home import HomeBanner, HomeFeature, HomeStory

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
        if not obj.images.exists():
            return ''
        return obj.images.first().image


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
        if not obj.images.exists():
            return ''

        img = obj.images.first()
        return img.image


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
        if not obj.images.exists():
            return ''

        img = obj.images.first()
        file_field = getattr(img, 'image', None)

        return img.image

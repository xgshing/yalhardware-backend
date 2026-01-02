# Serializer（后台 CRUD 用）
# apps/content/serializers/admin/home.py
from rest_framework import serializers
from ...models.home import HomeBanner, HomeFeature, HomeStory
from .image import (
    HomeBannerImageSerializer,
    HomeFeatureImageSerializer,
    HomeStoryImageSerializer,
)

# ================= HomeBanner =================
class AdminHomeBannerSerializer(serializers.ModelSerializer):
    images = HomeBannerImageSerializer(many=True, read_only=True)

    class Meta:
        model = HomeBanner
        fields = '__all__'

# ================= HomeFeature =================
class AdminHomeFeatureSerializer(serializers.ModelSerializer):
    images = HomeFeatureImageSerializer(many=True, read_only=True)  # 注意这里用 images

    class Meta:
        model = HomeFeature
        fields = '__all__'

# ================= HomeStory =================
class AdminHomeStorySerializer(serializers.ModelSerializer):
    images = HomeStoryImageSerializer(many=True, read_only=True)  # 注意这里用 images

    class Meta:
        model = HomeStory
        fields = '__all__'


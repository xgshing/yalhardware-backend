# 多图片 Serializer（通用）
# apps/content/serializers/admin/image.py
from rest_framework import serializers
from ...models.home import HomeBannerImage, HomeFeatureImage, HomeStoryImage

class ImageBaseSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)

    def get_image_url(self, obj):
        request = self.context.get('request')
        if hasattr(obj, 'image') and obj.image:
            return request.build_absolute_uri(obj.image.url)
        if hasattr(obj, 'icon') and obj.icon:
            return request.build_absolute_uri(obj.icon.url)
        return ''

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


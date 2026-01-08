# apps/system/serializers/company.py
from rest_framework import serializers
from django.conf import settings
from core.upload import upload_image
from ..models.company import CompanyProfile, CompanyAboutImage


class CompanyAboutImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CompanyAboutImage
        fields = ['id', 'image', 'image_url', 'sort', 'company']
        extra_kwargs = {
            'company': {'write_only': True}
        }

    def get_image_url(self, obj):
        request = self.context.get('request')

        if not obj.image:
            return ''

        # Cloudinary / URL 字符串
        if isinstance(obj.image, str):
            return obj.image

        # 本地 ImageField
        try:
            return request.build_absolute_uri(obj.image.url)
        except Exception:
            return ''

    def create(self, validated_data):
        image_file = validated_data.pop('image', None)

        if image_file:
            if not settings.DATABASES['default']['ENGINE'].endswith('sqlite3'):
                validated_data['image'] = upload_image(
                    image_file, folder='company/about'
                )
            else:
                validated_data['image'] = image_file

        return super().create(validated_data)



class CompanyProfileSerializer(serializers.ModelSerializer):
    about_images = CompanyAboutImageSerializer(many=True, read_only=True)

    class Meta:
        model = CompanyProfile
        fields = '__all__'

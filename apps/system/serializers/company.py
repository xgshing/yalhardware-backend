# apps/system/serializers/company.py
from rest_framework import serializers
from django.conf import settings
from core.cloudinary import upload_image
from ..models.company import CompanyProfile, CompanyAboutImage


class CompanyAboutImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CompanyAboutImage
        fields = ['id', 'image', 'image_url', 'sort']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if hasattr(obj, 'image') and obj.image:
            return request.build_absolute_uri(obj.image.url)
        return ''

    def create(self, validated_data):
        image_file = validated_data.pop('image', None)
        if image_file:
            if not settings.DATABASES['default']['ENGINE'].endswith('sqlite3'):
                validated_data['image'] = upload_image(image_file, folder='company/about')
            else:
                validated_data['image'] = image_file
        return super().create(validated_data)

    def update(self, instance, validated_data):
        image_file = validated_data.pop('image', None)
        if image_file:
            if not settings.DATABASES['default']['ENGINE'].endswith('sqlite3'):
                instance.image = upload_image(image_file, folder='company/about')
            else:
                instance.image = image_file
        return super().update(instance, validated_data)


class CompanyProfileSerializer(serializers.ModelSerializer):
    about_images = CompanyAboutImageSerializer(many=True, read_only=True)

    class Meta:
        model = CompanyProfile
        fields = '__all__'

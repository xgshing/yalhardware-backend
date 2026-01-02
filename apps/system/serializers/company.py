# apps/system/serializers/company.py
from rest_framework import serializers
from ..models.company import CompanyProfile, CompanyAboutImage

class CompanyAboutImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyAboutImage
        fields = ['id', 'image', 'sort']


class CompanyProfileSerializer(serializers.ModelSerializer):
    about_images = CompanyAboutImageSerializer(many=True, read_only=True)

    class Meta:
        model = CompanyProfile
        fields = '__all__'

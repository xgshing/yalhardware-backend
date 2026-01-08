# apps/system/views/company.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from core.upload import upload_image

from ..models.company import CompanyProfile, CompanyAboutImage
from ..serializers.company import CompanyProfileSerializer, CompanyAboutImageSerializer


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def company_profile(request):
    profile, _ = CompanyProfile.objects.get_or_create(id=1)

    if request.method == 'GET':
        serializer = CompanyProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)

    # POST / 更新
    serializer = CompanyProfileSerializer(
        profile,
        data=request.data,
        partial=True,
        context={'request': request}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def upload_company_about_image(request):
    company = CompanyProfile.objects.first()
    if not company:
        company = CompanyProfile.objects.create()

    image_file = request.FILES.get('image')
    if not image_file:
        return Response({'error': 'No image'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = CompanyAboutImageSerializer(
        data={
            'company': company.id,
            'image': image_file,
            'sort': request.data.get('sort', 0),
        },
        context={'request': request}
    )

    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)
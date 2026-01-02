# apps/system/views/company.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..models.company import CompanyProfile
from ..serializers.company import CompanyProfileSerializer


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])   
def company_profile(request):
    profile, _ = CompanyProfile.objects.get_or_create(id=1)

    if request.method == 'GET':
        serializer = CompanyProfileSerializer(profile)
        return Response(serializer.data)

    serializer = CompanyProfileSerializer(
        profile,
        data=request.data,
        partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

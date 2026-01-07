# apps/system/views/upload.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from core.cloudinary import upload_image

from ..models.rich_image import RichTextImage


@api_view(['POST'])
@permission_classes([AllowAny])
def upload_rich_image(request):
    """
    上传富文本编辑器图片
    """
    file = request.FILES.get('image')
    if not file:
        return Response({'error': 'No image'}, status=status.HTTP_400_BAD_REQUEST)

    # 上传处理
    if not settings.DATABASES['default']['ENGINE'].endswith('sqlite3'):
        file = upload_image(file, folder='richtext')

    img = RichTextImage.objects.create(image=file)

    return Response({
        'url': request.build_absolute_uri(img.image.url)
    }, status=status.HTTP_201_CREATED)


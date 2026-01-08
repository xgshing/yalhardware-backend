# apps/system/views/upload.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings

from core.upload import upload_image
from ..models.rich_image import RichTextImage


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_rich_image(request):
    """
    富文本图片上传
    - 本地：media/richtext/
    - 生产：Cloudinary
    - 返回：{ url: "..." }
    """
    file = request.FILES.get('image') or request.FILES.get('file')

    if not file:
        return Response(
            {'detail': 'No image uploaded'},
            status=400
        )

    # ===== 存储分流（与 CompanyAboutImage 完全一致）=====
    if not settings.DATABASES['default']['ENGINE'].endswith('sqlite3'):
        image_url = upload_image(file, folder='richtext')
        # 生产环境：存 URL
        rich_image = RichTextImage.objects.create(image=image_url)
    else:
        # 本地环境：存文件
        rich_image = RichTextImage.objects.create(image=file)
        image_url = request.build_absolute_uri(rich_image.image.url)

    return Response({
        'url': image_url
    })

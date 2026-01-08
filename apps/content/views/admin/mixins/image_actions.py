# apps/content/views/admin/mixins/image_actions.py
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from core.upload import upload_image

class MultiImageActionsMixin:
    """
    多图管理 Mixin：
    - create/update 时处理上传的 images
    - 删除不再使用的 existing_images
    - 排序 images
    - 单独上传接口
    """
    image_model = None       # 子类必须指定图片模型
    image_fk_field = None    # 外键字段名
    file_field = 'image'     # 默认图片字段名，可子类覆盖
    cloud_folder = 'home'    # Cloudinary folder，可子类覆盖

    def _upload_file(self, file):
        """根据环境上传图片"""
        if settings.DATABASES['default']['ENGINE'].endswith('sqlite3'):
            # 本地开发，直接保存文件
            return file
        # 生产环境上传 Cloudinary
        return upload_image(file, folder=self.cloud_folder)

    def _handle_images(self, instance):
        """处理 FormData 上传、existing_images 删除"""
        existing_ids = self.request.data.getlist('existing_images')
        qs = self.image_model.objects.filter(**{self.image_fk_field: instance})
        if existing_ids:
            qs.exclude(id__in=existing_ids).delete()
        else:
            qs.delete()

        files = self.request.FILES.getlist('images')  # 前端统一传 images
        for i, f in enumerate(files):
            url_or_file = self._upload_file(f)
            self.image_model.objects.create(
                **{
                    self.image_fk_field: instance,
                    self.file_field: url_or_file,
                    'order': i,
                }
            )

    def perform_create(self, serializer):
        instance = serializer.save()
        self._handle_images(instance)
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        self._handle_images(instance)
        return instance

    # ========== 排序接口 ==========
    @action(detail=True, methods=['post'])
    def sort_images(self, request, pk=None):
        if not isinstance(request.data, list):
            return Response({'error': 'Invalid payload, expected list'}, status=status.HTTP_400_BAD_REQUEST)
        for item in request.data:
            self.image_model.objects.filter(id=item['id']).update(order=item['order'])
        return Response({'success': True})

    # ========== 单独上传接口 ==========
    @action(detail=True, methods=['post'])
    def images(self, request, pk=None):
        parent = self.get_object()
        files = request.FILES.getlist('images')
        objs = []
        for i, f in enumerate(files):
            url_or_file = self._upload_file(f)
            objs.append(
                self.image_model(
                    **{
                        self.image_fk_field: parent,
                        self.file_field: url_or_file,
                        'order': i,
                    }
                )
            )
        self.image_model.objects.bulk_create(objs)
        return Response({'success': True})

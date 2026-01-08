# apps/products/views_admin.py
import json
import os
from urllib.parse import urlparse

from django.conf import settings
from django.core.files.storage import default_storage
from django.db import transaction
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

from .models import Product, ProductCategory, ProductVariant, ProductImage
from .serializers.product_create import ProductCreateSerializer
from .serializers.product_update import ProductUpdateSerializer
from .serializers.product_detail import ProductDetailSerializer
from .serializers.category import ProductCategorySerializer
from .serializers.category_tree import CategoryTreeSerializer

from core.upload import upload_image  # 统一入口，区分 DEBUG / PROD 上传


# ================= 工具函数 =================

def normalize_media_path(url: str) -> str:
    """
    将完整 URL 或 Cloudinary URL 转成本地相对路径
    主要用于删除本地文件
    """
    if not url:
        return url
    parsed = urlparse(url)
    path = parsed.path
    if path.startswith(settings.MEDIA_URL):
        return path.replace(settings.MEDIA_URL, '', 1)
    return path.lstrip('/')


# ================= 管理后台产品 =================

class AdminProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-is_featured', 'featured_order', 'id')
    permission_classes = [permissions.AllowAny]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ProductDetailSerializer
        if self.action in ['update', 'partial_update']:
            return ProductUpdateSerializer
        return ProductCreateSerializer

    # ========== 创建产品 ==========
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()

        # --------- 主图 cover ---------
        cover_file = request.FILES.get('cover')
        if cover_file:
            if settings.DEBUG:
                path = default_storage.save(f'products/covers/{cover_file.name}', cover_file)
                product.cover = path
            else:
                product.cover = upload_image(cover_file, 'products/covers')
            product.save(update_fields=['cover'])

        # --------- 详情图 detail_images ---------
        for img in request.FILES.getlist('uploaded_images'):
            if settings.DEBUG:
                path = default_storage.save(f'products/details/{img.name}', img)
                ProductImage.objects.create(product=product, image=path)
            else:
                url = upload_image(img, 'products/details')
                ProductImage.objects.create(product=product, image=url)

        # --------- 款式 variants ---------
        variants_raw = request.data.get('uploaded_variants')
        if variants_raw:
            try:
                variants_data = json.loads(variants_raw)
            except json.JSONDecodeError:
                return Response({'detail': 'uploaded_variants 格式错误'},
                                status=status.HTTP_400_BAD_REQUEST)

            for v in variants_data:
                uid = v.get('uid')
                image_file = request.FILES.get(f'uploaded_variants_images_{uid}')
                style_image = None

                if settings.DEBUG and image_file:
                    style_image = default_storage.save(f'products/variants/{image_file.name}', image_file)
                elif image_file:
                    style_image = upload_image(image_file, 'products/variants')

                ProductVariant.objects.create(
                    product=product,
                    style_name=v.get('style_name', ''),
                    spec=v.get('spec', ''),
                    stock=int(v.get('stock', 0)),
                    style_image=style_image
                )

        return Response({'id': product.id, 'message': '产品创建成功'}, status=status.HTTP_201_CREATED)

    # ========== 推荐产品排序 ==========
    @action(detail=False, methods=['post'], url_path='reorder')
    @transaction.atomic
    def reorder(self, request):
        data = request.data
        if not isinstance(data, list):
            return Response({'detail': '请求数据必须为列表'}, status=400)

        for item in data:
            pid = int(item.get('id'))
            order = int(item.get('featured_order', 0))
            Product.objects.filter(id=pid).update(featured_order=order)

        return Response({'message': '排序已保存'}, status=200)

    # ========== 更新产品 ==========
    def update(self, request, *args, **kwargs):
        product = self.get_object()

        # --------- 0️⃣ 更新基础字段 ---------
        serializer = self.get_serializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # --------- 1️⃣ 更新主图 cover ---------
        cover_file = request.FILES.get('cover')
        if cover_file:
            if settings.DEBUG:
                path = default_storage.save(f'products/covers/{cover_file.name}', cover_file)
                product.cover = path
            else:
                product.cover = upload_image(cover_file, 'products/covers')
            product.save(update_fields=['cover'])
        elif request.data.get('cover') == '':
            product.cover = None
            product.save(update_fields=['cover'])

        # --------- 2️⃣ 删除 detail_images ---------
        removed_images_raw = request.data.get('removed_detail_images', '[]')
        try:
            removed_images = json.loads(removed_images_raw)
        except json.JSONDecodeError:
            removed_images = []

        if removed_images:
            for url in removed_images:
                # 本地环境，把完整 URL 转成相对路径
                if settings.DEBUG and url.startswith(request.build_absolute_uri(settings.MEDIA_URL)):
                    url = url.replace(request.build_absolute_uri(settings.MEDIA_URL), '')

                try:
                    img_obj = ProductImage.objects.get(product=product, image=url)
                    # 本地删除文件
                    if settings.DEBUG and img_obj.image:
                        default_storage.delete(img_obj.image)
                    img_obj.delete()
                except ProductImage.DoesNotExist:
                    continue

        # --------- 3️⃣ 新增 detail_images ---------
        for img in request.FILES.getlist('uploaded_images'):
            if settings.DEBUG:
                path = default_storage.save(f'products/details/{img.name}', img)
                ProductImage.objects.create(product=product, image=path)
            else:
                url = upload_image(img, 'products/details')
                ProductImage.objects.create(product=product, image=url)

        # --------- 4️⃣ variants（增 / 改 / 删 / 图） ---------
        variants_raw = request.data.get('uploaded_variants')
        if variants_raw:
            try:
                variants_data = json.loads(variants_raw)
            except json.JSONDecodeError:
                return Response({'detail': 'uploaded_variants 格式错误'},
                                status=status.HTTP_400_BAD_REQUEST)

            keep_ids = []

            for v in variants_data:
                vid = v.get('id')
                uid = v.get('uid')
                remove_image = v.get('remove_image', False)
                image_file = request.FILES.get(f'uploaded_variants_images_{uid}')
                style_image = None

                if vid:
                    obj = ProductVariant.objects.get(id=vid, product=product)
                    obj.style_name = v.get('style_name', '')
                    obj.spec = v.get('spec', '')
                    obj.stock = int(v.get('stock', 0))

                    # 删除图片
                    if remove_image:
                        obj.style_image = None

                    # 替换图片
                    if image_file:
                        if settings.DEBUG:
                            style_image = default_storage.save(f'products/variants/{image_file.name}', image_file)
                        else:
                            style_image = upload_image(image_file, 'products/variants')
                        obj.style_image = style_image

                    obj.save(update_fields=['style_name', 'spec', 'stock', 'style_image'])
                    keep_ids.append(obj.id)
                else:
                    # 新增 variant
                    if settings.DEBUG and image_file:
                        style_image = default_storage.save(f'products/variants/{image_file.name}', image_file)
                    elif image_file:
                        style_image = upload_image(image_file, 'products/variants')

                    obj = ProductVariant.objects.create(
                        product=product,
                        style_name=v.get('style_name', ''),
                        spec=v.get('spec', ''),
                        stock=int(v.get('stock', 0)),
                        style_image=style_image
                    )
                    keep_ids.append(obj.id)

            # 删除被移除的款式
            to_delete = ProductVariant.objects.filter(product=product).exclude(id__in=keep_ids)
            for v in to_delete:
                if settings.DEBUG and v.style_image:
                    default_storage.delete(v.style_image)
                v.delete()

        # --------- 5️⃣ 强制重新查询并返回 ---------
        product = Product.objects.prefetch_related('detail_images', 'variants').get(id=product.id)
        serializer = ProductDetailSerializer(product, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


# ================= 分类 =================

class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get'], url_path='tree')
    def tree(self, request):
        roots = ProductCategory.objects.filter(parent__isnull=True)
        serializer = CategoryTreeSerializer(roots, many=True)
        return Response(serializer.data)

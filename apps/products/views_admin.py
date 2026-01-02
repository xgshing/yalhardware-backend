# products/views_admin.py
import json
import os
from django.conf import settings
from django.db import transaction

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import JSONParser,MultiPartParser, FormParser

from .models import (
    Product,
    ProductCategory,
    ProductVariant,
    ProductImage,
)

from .serializers.product_create import ProductCreateSerializer
from .serializers.product_update import ProductUpdateSerializer
from .serializers.product_detail import ProductDetailSerializer
from .serializers.category import ProductCategorySerializer
from .serializers.category_tree import CategoryTreeSerializer



# ================= 工具函数 =================

from urllib.parse import urlparse

def normalize_media_path(url: str) -> str:
    """
    支持：
    - /media/xxx.jpg
    - http://localhost:8000/media/xxx.jpg
    """
    if not url:
        return url

    parsed = urlparse(url)
    path = parsed.path  # 只取 /media/xxx.jpg

    if path.startswith(settings.MEDIA_URL):
        return path.replace(settings.MEDIA_URL, '', 1)

    return path.lstrip('/')



def delete_file(field):
    """
    安全删除 ImageField 对应的文件
    """
    if field and hasattr(field, 'path') and os.path.exists(field.path):
        os.remove(field.path)


# ================= 管理后台产品 =================

class AdminProductViewSet(viewsets.ModelViewSet):
    # 产品排序
    queryset = Product.objects.all().order_by(
        '-is_featured',
        'featured_order',
        'id'
    )
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

        # 详情图
        for img in request.FILES.getlist('uploaded_images'):
            ProductImage.objects.create(product=product, image=img)

        # variants
        variants_raw = request.data.get('uploaded_variants')
        if variants_raw:
            try:
                variants_data = json.loads(variants_raw)
            except json.JSONDecodeError:
                return Response(
                    {'detail': 'uploaded_variants 格式错误'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            for v in variants_data:
                uid = v.get('uid')
                image = request.FILES.get(f'uploaded_variants_images_{uid}')

                ProductVariant.objects.create(
                    product=product,
                    style_name=v.get('style_name'),
                    spec=v.get('spec', ''),
                    stock=v.get('stock', 0),
                    style_image=image
                )

        return Response(
            {'id': product.id, 'message': '产品创建成功'},
            status=status.HTTP_201_CREATED
        )


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


    # ========== 更新产品（核心逻辑全集中） ==========
    # products/views_admin.py

    def update(self, request, *args, **kwargs):
        product = self.get_object()

        # ===============================
        # 0️⃣ 更新 Product 基础字段
        # ===============================
        serializer = self.get_serializer(
            product,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # ===============================
        # 1️⃣ 删除主图
        # ===============================
        if request.data.get('cover') == '':
            if product.cover:
                product.cover.delete(save=False)
                product.cover = None
                product.save(update_fields=['cover'])

        # ===============================
        # 2️⃣ 删除详情图（文件 + DB）
        # ===============================
        removed_images_raw = request.data.get('removed_detail_images', '[]')
        try:
            removed_images = json.loads(removed_images_raw)
        except json.JSONDecodeError:
            removed_images = []

        if removed_images:
            paths = [normalize_media_path(u) for u in removed_images]
            images = ProductImage.objects.filter(
                product=product,
                image__in=paths
            )

            for img in images:
                if img.image:
                    img.image.delete(save=False)
                img.delete()

        # ===============================
        # 3️⃣ 新增详情图
        # ===============================
        for img in request.FILES.getlist('uploaded_images'):
            ProductImage.objects.create(product=product, image=img)

        # ===============================
        # 4️⃣ 款式（增 / 改 / 删 / 图）
        # ===============================
        variants_raw = request.data.get('uploaded_variants')

        if variants_raw:
            try:
                variants_data = json.loads(variants_raw)
            except json.JSONDecodeError:
                return Response(
                    {'detail': 'uploaded_variants 格式错误'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            keep_ids = []

            for v in variants_data:
                vid = v.get('id')
                uid = v.get('uid')
                remove_image = v.get('remove_image', False)

                image = request.FILES.get(f'uploaded_variants_images_{uid}')

                if vid:
                    # ===== 更新 =====
                    obj = ProductVariant.objects.get(
                        id=vid,
                        product=product
                    )

                    # ⭐ 所有字段都明确赋值（关键）
                    obj.style_name = v.get('style_name', '')
                    obj.spec = v.get('spec', '')
                    obj.stock = int(v.get('stock', 0))

                    # 删除图片
                    if remove_image:
                        if obj.style_image:
                            obj.style_image.delete(save=False)
                            obj.style_image = None

                    # 替换图片
                    if image:
                        if obj.style_image:
                            obj.style_image.delete(save=False)
                        obj.style_image = image

                    obj.save()
                    keep_ids.append(obj.id)

                else:
                    # ===== 新增 =====
                    obj = ProductVariant.objects.create(
                        product=product,
                        style_name=v.get('style_name', ''),
                        spec=v.get('spec', ''),
                        stock=int(v.get('stock', 0)),
                        style_image=image if image else None
                    )
                    keep_ids.append(obj.id)

            # ===== 删除被移除的款式（文件 + DB）=====
            to_delete = ProductVariant.objects.filter(
                product=product
            ).exclude(id__in=keep_ids)

            for v in to_delete:
                if v.style_image:
                    v.style_image.delete(save=False)
                v.delete()

        # ===============================
        # 5️⃣ 强制重新查询（核心修复）
        # ===============================
        product = (
            Product.objects
            .prefetch_related('detail_images', 'variants')
            .get(id=product.id)
        )

        serializer = ProductDetailSerializer(
            product,
            context={'request': request}
        )

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

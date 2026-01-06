# apps/products/views_admin.py
import json
from django.db import transaction
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

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

from core.cloudinary import upload_image


# =========================
# 后台产品管理（Cloudinary 版）
# =========================
class AdminProductViewSet(viewsets.ModelViewSet):
    """
    ✅ Cloudinary 版后台产品管理
    - 所有图片上传 Cloudinary
    - 数据库只存 URL
    """
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

    # =========================
    # 创建产品
    # =========================
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = serializer.save()

        # ===== 1️⃣ 主图 =====
        cover_file = request.FILES.get('cover')
        if cover_file:
            product.cover = upload_image(
                cover_file,
                folder='yalhardware/products/cover'
            )
            product.save(update_fields=['cover'])

        # ===== 2️⃣ 详情图 =====
        for img in request.FILES.getlist('uploaded_images'):
            url = upload_image(
                img,
                folder='yalhardware/products/detail'
            )
            ProductImage.objects.create(
                product=product,
                image=url
            )

        # ===== 3️⃣ 款式 =====
        variants_raw = request.data.get('uploaded_variants')
        if variants_raw:
            variants_data = json.loads(variants_raw)
            for v in variants_data:
                uid = v.get('uid')
                file = request.FILES.get(f'uploaded_variants_images_{uid}')

                image_url = None
                if file:
                    image_url = upload_image(
                        file,
                        folder='yalhardware/products/variants'
                    )

                ProductVariant.objects.create(
                    product=product,
                    style_name=v.get('style_name', ''),
                    spec=v.get('spec', ''),
                    stock=int(v.get('stock', 0)),
                    style_image=image_url
                )

        return Response(
            {'id': product.id, 'message': '产品创建成功'},
            status=status.HTTP_201_CREATED
        )

    # =========================
    # 更新产品
    # =========================
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        product = self.get_object()

        # ===== 0️⃣ 基础字段 =====
        serializer = self.get_serializer(
            product,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # ===== 1️⃣ 主图 =====
        if request.data.get('cover') == '':
            product.cover = None
            product.save(update_fields=['cover'])

        cover_file = request.FILES.get('cover')
        if cover_file:
            product.cover = upload_image(
                cover_file,
                folder='yalhardware/products/cover'
            )
            product.save(update_fields=['cover'])

        # ===== 2️⃣ 删除详情图 =====
        removed_raw = request.data.get('removed_detail_images', '[]')
        removed = json.loads(removed_raw)

        if removed:
            ProductImage.objects.filter(
                product=product,
                image__in=removed
            ).delete()

        # ===== 3️⃣ 新增详情图 =====
        for img in request.FILES.getlist('uploaded_images'):
            url = upload_image(
                img,
                folder='yalhardware/products/detail'
            )
            ProductImage.objects.create(
                product=product,
                image=url
            )

        # ===== 4️⃣ 款式增改删 =====
        variants_raw = request.data.get('uploaded_variants')
        if variants_raw:
            variants_data = json.loads(variants_raw)
            keep_ids = []

            for v in variants_data:
                vid = v.get('id')
                uid = v.get('uid')
                remove_image = v.get('remove_image', False)
                file = request.FILES.get(f'uploaded_variants_images_{uid}')

                if vid:
                    obj = ProductVariant.objects.get(
                        id=vid,
                        product=product
                    )
                    obj.style_name = v.get('style_name', '')
                    obj.spec = v.get('spec', '')
                    obj.stock = int(v.get('stock', 0))

                    if remove_image:
                        obj.style_image = None

                    if file:
                        obj.style_image = upload_image(
                            file,
                            folder='yalhardware/products/variants'
                        )

                    obj.save()
                    keep_ids.append(obj.id)

                else:
                    image_url = None
                    if file:
                        image_url = upload_image(
                            file,
                            folder='yalhardware/products/variants'
                        )

                    obj = ProductVariant.objects.create(
                        product=product,
                        style_name=v.get('style_name', ''),
                        spec=v.get('spec', ''),
                        stock=int(v.get('stock', 0)),
                        style_image=image_url
                    )
                    keep_ids.append(obj.id)

            # 删除未保留款式
            ProductVariant.objects.filter(
                product=product
            ).exclude(id__in=keep_ids).delete()

        # ===== 5️⃣ 返回最新数据 =====
        product = (
            Product.objects
            .prefetch_related('detail_images', 'variants')
            .get(id=product.id)
        )

        serializer = ProductDetailSerializer(
            product,
            context={'request': request}
        )
        return Response(serializer.data)

    # =========================
    # 推荐产品排序
    # =========================
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


# =========================
# 产品分类管理
# =========================
class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get'], url_path='tree')
    def tree(self, request):
        roots = ProductCategory.objects.filter(parent__isnull=True)
        serializer = CategoryTreeSerializer(roots, many=True)
        return Response(serializer.data)

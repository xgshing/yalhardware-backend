# apps/products/models.py
# 提供各种字段类型（CharField、IntegerField 等）用来定义数据库表（Model）
from django.db import models

# ProductCategory（分类模型）
class ProductCategory(models.Model):
    # 产品分类.unique=True 分类名称唯一
    name = models.CharField(max_length=100, unique=True)
    # 父分类（小类指向主分类） parent = null主分类。parent ≠ null	子分类（小类）
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        on_delete=models.CASCADE,
    )
    # 加排序字段
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.name
    
# Product（产品模型）
class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        'ProductCategory',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='products'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    specifications = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    featured_order = models.IntegerField(default=0)

    # ✅ 改为 URLField
    cover = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    """
    产品款式，例如颜色、型号、尺寸等
    """
    product = models.ForeignKey(
        Product,
        related_name='variants',
        on_delete=models.CASCADE
    )
    style_name = models.CharField(max_length=255, blank=True)
    spec = models.CharField(max_length=255, blank=True)
    stock = models.IntegerField(default=0)

    # ✅ 改为 URLField
    style_image = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Variant of {self.product_id}"



class ProductImage(models.Model):
    """
    产品详情图（多图）
    外键关联 Product
    related_name='detail_images' → 允许通过 product.detail_images.all() 获取所有详情图
    on_delete=models.CASCADE → 产品删除时，关联的详情图也自动删除
    """
    product = models.ForeignKey(
        Product,
        related_name='detail_images',
        on_delete=models.CASCADE
    )
    # ✅ 改为 URLField
    image = models.URLField()

    def __str__(self):
        return f"Image of {self.product_id}"

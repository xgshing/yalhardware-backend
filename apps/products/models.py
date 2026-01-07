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
    # 产品名称.CharField 用于存储短文本,max_length=255 限制数据库列最大长度
    name = models.CharField(max_length=255)
     # 外键指向 ProductCategory，运营者可以新增分类
    category = models.ForeignKey(
        ProductCategory,
        related_name='products',
        on_delete=models.PROTECT,  
        blank=True,
        null=True
    )

    # 价格字段.DecimalField 精确存储小数，适合财务数据,max_digits=10 → 总共 10 位数字,decimal_places=2 → 小数点 2 位
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # 产品描述.TextField 用于长文本,blank=True → 在表单中可以为空
    description = models.TextField(blank=True)
    specifications = models.TextField(blank=True)
    # 是否上架.前端页面或后台管理可根据此字段决定是否显示
    is_active = models.BooleanField(default=True)

    # 是否推荐产品（首页或活动页展示）
    is_featured = models.BooleanField(default=False)
    featured_order = models.PositiveIntegerField(default=0)  # 推荐顺序（整数）
    
    # 主图。upload_to 指定上传路径,blank=True → 表单可为空,null=True → 数据库允许 NULL
    cover = models.ImageField(
        upload_to='products/covers/',
        blank=True,
        null=True
    )

    # 推荐指数排序（越小越靠前）
    featured_rank = models.IntegerField(null=True, blank=True)
    #创建时间。auto_now_add=True → 自动设置为当前时间，创建后不可修改
    created_at = models.DateTimeField(auto_now_add=True)

    # Django Admin 显示对象的可读字符串直接显示产品名称，便于后台管理查看
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
    style_name = models.CharField(max_length=100)  # 款式名称，如“红色”、“黑色”
    style_image = models.ImageField(upload_to='products/variants/')
    spec = models.CharField(max_length=100, blank=True)  # 规格/尺寸，如“XL”、“20cm”
    stock = models.IntegerField(default=0)  # 每个款式的库存

    # 销售量.默认值为 0，可用于统计热销产品
    sales_volume = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.style_name} ({self.spec})"



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
    # 存储详情图.upload_to='products/details/' → 上传到对应目录
    image = models.ImageField(upload_to='products/details/')

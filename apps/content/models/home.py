# models（首页内容模型）
# apps/content/models/home.py
from django.db import models
from .mixins import ImageMixin


class HomeBanner(models.Model):
    title = models.CharField('主标题', max_length=200)
    description = models.TextField('副标题/说明', blank=True)

    button_text = models.CharField(
        '按钮文字', max_length=50, blank=True
    )
    button_link = models.CharField(
        '按钮链接', max_length=255, blank=True
    )

    order = models.PositiveIntegerField('排序', default=0)
    is_active = models.BooleanField('是否启用', default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '首页轮播'
        verbose_name_plural = '首页轮播'
        ordering = ['order']

    def __str__(self):
        return self.title


class HomeBannerImage(ImageMixin):
    banner = models.ForeignKey(
        HomeBanner,
        related_name='images',
        on_delete=models.CASCADE,
    )
    image = models.URLField('图片URL', max_length=500)

# ==============================================================
class HomeFeature(models.Model):
    title = models.CharField('标题', max_length=100)
    description = models.TextField('描述')

    order = models.PositiveIntegerField('排序', default=0)
    is_active = models.BooleanField('是否启用', default=True)

    class Meta:
        verbose_name = '首页核心卖点'
        verbose_name_plural = '首页核心卖点'
        ordering = ['order']

    def __str__(self):
        return self.title


class HomeFeatureImage(ImageMixin):
    feature = models.ForeignKey(
        HomeFeature,
        related_name='images',          # 外键反向查询名
        on_delete=models.CASCADE,
    )
    image = models.URLField('图片URL', max_length=500)

# ==============================================================
class HomeStory(models.Model):
    title = models.CharField('标题', max_length=150)
    description = models.TextField('描述')

    order = models.PositiveIntegerField('排序', default=0)
    is_active = models.BooleanField('是否启用', default=True)

    class Meta:
        verbose_name = '首页品牌理念'
        verbose_name_plural = '首页品牌理念'
        ordering = ['order']

    def __str__(self):
        return self.title


class HomeStoryImage(ImageMixin):
    story = models.ForeignKey(
        HomeStory,
        related_name='images',  
        on_delete=models.CASCADE,
    )
    image = models.URLField('图片URL', max_length=500)
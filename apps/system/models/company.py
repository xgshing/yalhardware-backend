# apps/system/models/company.py
from django.db import models

# apps/system/models/company.py

from django.db import models

class CompanyProfile(models.Model):
    # ===== 联系方式 =====
    company_name = models.CharField('公司名称', max_length=255, blank=True)
    address = models.TextField('公司地址', blank=True)
    contact_person = models.CharField('联系人', max_length=100, blank=True)
    mobile = models.CharField('手机 / WeChat', max_length=50, blank=True)
    email = models.EmailField('邮箱', blank=True)

    # ===== 公司介绍（富文本）=====
    about_html = models.TextField('公司介绍（富文本）', blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '公司信息'
        verbose_name_plural = '公司信息'

    def __str__(self):
        return self.company_name or 'Company Profile'


# 多图上传，独立表
class CompanyAboutImage(models.Model):
    company = models.ForeignKey(
        CompanyProfile,
        related_name='about_images',
        on_delete=models.CASCADE
    )
    image = models.URLField(max_length=500)
    sort = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort']

# 设置多图
# apps/content/models/mixins.py
from django.db import models


class ImageMixin(models.Model):
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['order', '-id']

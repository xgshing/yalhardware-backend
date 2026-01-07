# apps/system/models/rich_image.py
from django.db import models

class RichTextImage(models.Model):
    image = models.ImageField(upload_to='richtext/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.url

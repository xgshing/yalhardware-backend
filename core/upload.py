# core/upload.py 
# 直接返回 URL 的工具
import os
import uuid
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


def upload_image(file, folder: str) -> str:
    """
    返回：可直接给前端用的 URL
    """
    if settings.DEBUG:
        ext = os.path.splitext(file.name)[1]
        filename = f"{folder}/{uuid.uuid4()}{ext}"
        path = default_storage.save(filename, ContentFile(file.read()))
        return settings.MEDIA_URL + path        # ← 返回 URL 字符串

    else:
        from cloudinary.uploader import upload
        res = upload(file, folder=folder)
        return res['secure_url']            # ← 返回 Cloudinary URL
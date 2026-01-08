# core/upload.py
# 统一上传工具（本地 / 生产自动分流）
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
        return settings.MEDIA_URL + path

    else:
        from cloudinary.uploader import upload
        res = upload(file, folder=folder)
        return res['secure_url']

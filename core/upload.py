# core/upload.py
import os
import uuid
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


def upload_image(file, folder: str) -> str:
    """
    永远返回【完整可访问 URL】
    """
    ext = os.path.splitext(file.name)[1]
    filename = f"{folder}/{uuid.uuid4()}{ext}"

    if settings.DEBUG:
        path = default_storage.save(filename, ContentFile(file.read()))
        return settings.MEDIA_URL + path   # "/media/home/xxx.jpg"

    from cloudinary.uploader import upload
    res = upload(file, folder=folder)
    return res['secure_url']

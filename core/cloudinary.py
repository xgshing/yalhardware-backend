# Cloudinary 上传工具函数
# core/cloudinary.py
import cloudinary.uploader
from django.conf import settings
import tempfile

def upload_image(file, folder="default"):
    """
    生产环境上传 Cloudinary，本地保留 media/
    返回最终保存给 ImageField 的值：
    - 本地：原始 file
    - 生产环境：Cloudinary URL
    """
    if getattr(settings, 'DATABASES', {}).get('default', {}).get('ENGINE', '').endswith('postgresql'):
        # 生产环境：上传 Cloudinary
        result = cloudinary.uploader.upload(file, folder=folder, resource_type="image")
        # Cloudinary URL 转 bytes 保存在 ImageField
        # 这里直接返回 URL 字符串，ImageField 支持存 URL
        return result["secure_url"]
    else:
        # 本地：直接返回文件
        return file

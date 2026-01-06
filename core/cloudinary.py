# Cloudinary 上传工具函数
# BACKEND/core/cloudinary.py
import cloudinary.uploader

def upload_image(file, folder="products"):
    result = cloudinary.uploader.upload(
        file,
        folder=folder,
        resource_type="image"
    )
    return result["secure_url"]

# apps/system/urls.py
from django.urls import path
from ..views.company import company_profile
from ..views.upload import upload_rich_image

urlpatterns = [
    path('company/profile/', company_profile),
    path('upload/rich-image/', upload_rich_image),
]

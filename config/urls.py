# config/urls.py
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

# Django REST framework（DRF）后端里，没有像 Postman 或 Swagger 那样
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.products.urls')),
    path('api/', include('apps.content.urls.frontend')),
    path('api/admin/', include('apps.content.urls.admin')),
    path('api/', include('apps.system.urls.company')),
    
]


# Django REST framework（DRF）后端里，没有像 Postman 或 Swagger 那样
# Swagger schema 配置
schema_view = get_schema_view(
   openapi.Info(
      title="YAL Hardware API",
      default_version='v1',
      description="Frontend 可用的 API 文档",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # 你的 API
    path('api/products/', include('apps.products.urls')),  # 根据你的 apps 配置修改
    path('api/categories/', include('apps.categories.urls')),

    # Swagger / Redoc 文档
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# 只有 DEBUG=True 时才允许直接访问 media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
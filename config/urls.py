# config/urls.py
from django.contrib import admin
from django.urls import path, include

from core.views import health

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    # ===== 健康检查（监控专用）=====
    path('health/', health),

    # ===== API =====
    path('api/', include('apps.products.urls')),
    path('api/', include('apps.content.urls.frontend')),
    path('api/admin/', include('apps.content.urls.admin')),
    path('api/', include('apps.system.urls.company')),
    
]

# 只有 DEBUG=True 时才允许直接访问 media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
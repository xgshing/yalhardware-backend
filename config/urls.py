# config/urls.py
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.products.urls')),
    path('api/', include('apps.content.urls.frontend')),
    path('api/admin/', include('apps.content.urls.admin')),
    path('api/', include('apps.system.urls.company')),
    
]

# 只有 DEBUG=True 时才允许直接访问 media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
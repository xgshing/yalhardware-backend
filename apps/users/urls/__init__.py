# apps/users/urls/__init__.py
from django.urls import include, path

urlpatterns = [
    path("auth/", include("apps.users.urls.auth")),
    path("", include("apps.users.urls.me")),
    path("admin/", include("apps.users.urls.admin")),
]

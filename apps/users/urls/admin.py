# Admin 用户管理
# apps/users/urls/admin.py
from django.urls import path
from apps.users.views.admin import (
    AdminUserListView,
    AdminUserDetailView,
    AdminUserUpdateView,
)

urlpatterns = [
    path("", AdminUserListView.as_view()),
    path("<int:pk>/", AdminUserDetailView.as_view()),
    path("<int:user_id>/update/", AdminUserUpdateView.as_view()),
]

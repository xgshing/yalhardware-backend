# 注册 / 登录
# apps/users/urls/auth.py
from django.urls import path
from apps.users.views.auth import RegisterView, LoginView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
]

# apps/users/urls/me.py
from django.urls import path
from apps.users.views.me import UserMeView

urlpatterns = [
    path("me/", UserMeView.as_view()),
]

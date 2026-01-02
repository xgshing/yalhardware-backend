# apps/content/urls/frontend.py
from django.urls import path
from ..views.frontend.home import HomeAPIView

urlpatterns = [
    path('home/', HomeAPIView.as_view()),
]

# apps/orders/urls/frontend.py
from django.urls import path
from apps.orders.views.frontend.order_list import OrderListView
from apps.orders.views.frontend.order_submit import OrderSubmitView
from apps.orders.views.frontend.order_detail import OrderDetailView
from apps.orders.views.frontend.order_actions import (
    OrderCancelView,
    OrderPayView,
    OrderConfirmView,
)

urlpatterns = [
    path("", OrderListView.as_view()),
    path("submit/", OrderSubmitView.as_view()),
    path("<int:order_id>/", OrderDetailView.as_view()),
    path("<int:order_id>/cancel/", OrderCancelView.as_view()),
    path("<int:order_id>/pay/", OrderPayView.as_view()),
    path("<int:order_id>/confirm/", OrderConfirmView.as_view()),
]

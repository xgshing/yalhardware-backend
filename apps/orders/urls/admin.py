# apps/orders/urls/admin.py
from django.urls import path
from apps.orders.views.admin.order_list import AdminOrderListView
from apps.orders.views.admin.order_detail import AdminOrderDetailView
from apps.orders.views.admin.order_ship import AdminOrderShipView

urlpatterns = [
    path("orders/", AdminOrderListView.as_view()),
    path("orders/<int:order_id>/", AdminOrderDetailView.as_view()),
    path("orders/<int:order_id>/ship/", AdminOrderShipView.as_view()),
]

# apps/inventory/urls.py
from rest_framework.routers import DefaultRouter
from .views import InventoryRecordViewSet

router = DefaultRouter()
router.register(
    r"inventory-records", InventoryRecordViewSet, basename="inventory-record"
)

urlpatterns = router.urls

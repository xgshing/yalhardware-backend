# apps/reviews/urls/frontend.py
from rest_framework.routers import DefaultRouter
from apps.reviews.views.frontend.review import ReviewViewSet

router = DefaultRouter()
router.register(r"reviews", ReviewViewSet, basename="review")

urlpatterns = router.urls

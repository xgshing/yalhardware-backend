# apps/content/urls/admin.py
from rest_framework.routers import DefaultRouter
from ..views.admin.home import (
    AdminHomeBannerViewSet,
    AdminHomeFeatureViewSet,
    AdminHomeStoryViewSet,
)
from ..views.admin.home_images import (
    AdminHomeBannerImageViewSet,
    AdminHomeFeatureImageViewSet,
    AdminHomeStoryImageViewSet,
)

router = DefaultRouter()
router.register('home/banners', AdminHomeBannerViewSet)
router.register('home/features', AdminHomeFeatureViewSet)
router.register('home/stories', AdminHomeStoryViewSet)

# ---------------- 单图删除 ----------------
router.register('home/banner-images', AdminHomeBannerImageViewSet)
router.register('home/feature-images', AdminHomeFeatureImageViewSet)
router.register('home/story-images', AdminHomeStoryImageViewSet)

urlpatterns = router.urls

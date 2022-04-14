from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import ClientViewSet, MailViewSet

router = DefaultRouter()
router.register("clients", ClientViewSet, basename="clients")
router.register("mailings", MailViewSet, basename="mailings")

urlpatterns = [
    path("", include(router.urls)),
    re_path(r"^auth/", include("djoser.urls.authtoken")),
]

from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# router.register("users", UserViewSet)

urlpatterns = [
    path("referral/", include("referral_system.referral.urls")),
]

app_name = "api"
urlpatterns += router.urls

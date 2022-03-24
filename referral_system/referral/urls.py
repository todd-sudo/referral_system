from django.urls import path

from .views import (
    ActivateInviteCodeView,
    ProfileView,
    SendCodeSMSView,
    ActivateSMSCode
)


urlpatterns = [
    path("create-invite/", ActivateInviteCodeView.as_view(), name="create-invite"),
    path("profile/<str:id>/", ProfileView.as_view(), name="profile"),
    path("send-sms/", SendCodeSMSView.as_view(), name="send-sms"),
    path("auth-user/", ActivateSMSCode.as_view(), name="auth-user"),
]


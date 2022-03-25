from django.urls import path

from .views import (
    ActivateInviteCodeView,
    ProfileView,
    LoginSendCodeSMSView,
    ActivateSMSCode
)


urlpatterns = [
    path("activate-invite/", ActivateInviteCodeView.as_view(), name="activate-invite"),
    path("profile/<str:id>/", ProfileView.as_view(), name="profile"),
    path("login-sms/", LoginSendCodeSMSView.as_view(), name="login-sms"),
    path("sms-code/", ActivateSMSCode.as_view(), name="sms-code"),
]


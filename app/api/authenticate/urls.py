from django.urls import path

from api.authenticate.views import (
    CookieTokenObtainPairView,
    CookieTokenRefreshView,
    ResendingActivatingCodeApiView,
    ActivateAccountApiView,
    CheckActivationCodeApiView,
)

urlpatterns = [
    path('token/', CookieTokenObtainPairView.as_view(), name='token'),
    path('token_refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),

    path('auth/activate/', ActivateAccountApiView.as_view(), name='activate'),
    path('auth/check_activation_code/', CheckActivationCodeApiView.as_view(), name='check_activation_code'),
    path('auth/resend_code/', ResendingActivatingCodeApiView.as_view(), name='resend_code'),
]

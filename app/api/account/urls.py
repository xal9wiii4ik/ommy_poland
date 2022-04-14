from django.urls import path

from api.account.views import (
    RegisterUserApiView,
    ForgotPasswordApiView,
    UpdatePasswordApiView
)

urlpatterns = [
    path('account/register/', RegisterUserApiView.as_view(), name='register'),
    path('account/forgot_password/', ForgotPasswordApiView.as_view(), name='forgot_password'),
    path('account/update_password/', UpdatePasswordApiView.as_view(), name='update_password'),
]

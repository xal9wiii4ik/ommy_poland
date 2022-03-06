from django.urls import path

from apps.account.views import (
    RegisterUserApiView,
)

urlpatterns = [
    path('account/register/', RegisterUserApiView.as_view(), name='register'),
]

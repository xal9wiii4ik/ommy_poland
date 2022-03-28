from django.urls import path

from api.authenticate.views import CookieTokenObtainPairView, CookieTokenRefreshView

from api.authenticate.views import ActivateAccountApiView

urlpatterns = [
    path('token/', CookieTokenObtainPairView.as_view(), name='token'),
    path('token_refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),

    path('auth/activate/', ActivateAccountApiView.as_view(), name='activate'),
]

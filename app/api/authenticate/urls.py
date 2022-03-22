from django.urls import path

from api.authenticate.views import ActivateAccountApiView

urlpatterns = [
    path('activate/', ActivateAccountApiView.as_view(), name='activate'),
]

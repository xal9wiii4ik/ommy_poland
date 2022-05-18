from django.urls import path

from api.payments.views import CommissionApiView

urlpatterns = [
    path('create_commission/', CommissionApiView.as_view(), name='create_commission'),
]

from django.urls import path
from rest_framework.routers import SimpleRouter

from api.master.views import MasterModelViewSet, RegisterMasterApiView

router = SimpleRouter()

router.register('master', MasterModelViewSet)

urlpatterns = [
    path('master/register/', RegisterMasterApiView.as_view(), name='register'),
]

urlpatterns += router.urls

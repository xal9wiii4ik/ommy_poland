from django.urls import path
from rest_framework.routers import SimpleRouter

from api.master.views import (
    MasterModelViewSet,
    RegisterMasterApiView,
    WorkSphereModelViewSet,
    MasterExperienceModelViewSet,
)

router = SimpleRouter()

router.register('master', MasterModelViewSet)
router.register('work_sphere', WorkSphereModelViewSet)
router.register('master_experience', MasterExperienceModelViewSet)

urlpatterns = [
    path('master/register/', RegisterMasterApiView.as_view(), name='register'),
]

urlpatterns += router.urls

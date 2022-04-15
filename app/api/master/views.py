import typing as tp

from drf_yasg.utils import swagger_auto_schema

from rest_framework import status, mixins

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from api.master.models import Master, WorkSphere, MasterExperience
from api.master.permissions import IsOwnerMasterPermission, IsOwnerMasterExperiencePermission
from api.master.serializers import (
    MasterModelSerializer,
    MasterRegisterSerializer,
    WorkSphereModelSerializer,
    MasterExperienceModelSerializer,
)
from api.master.services import create_master_account
from api.utils.services import get_serializer_data


class RegisterMasterApiView(APIView):
    """
    View for register new master
    """

    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=MasterRegisterSerializer)
    def post(self, request: Request, *args: tp.Any, **kwargs: tp.Any) -> Response:
        serializer_data = get_serializer_data(data=request.data, serializer=MasterRegisterSerializer)

        user_pk = create_master_account(data=serializer_data, master_experiences=request.data.get('master_experience'))
        serializer_data.update({'user_pk': user_pk})
        return Response(data=serializer_data, status=status.HTTP_201_CREATED)


class WorkSphereModelViewSet(mixins.ListModelMixin,
                             GenericViewSet):
    """
    Model view set for model work sphere
    """

    serializer_class = WorkSphereModelSerializer
    queryset = WorkSphere.objects.all()
    permission_classes = (AllowAny,)


class MasterExperienceModelViewSet(mixins.ListModelMixin,
                                   mixins.CreateModelMixin,
                                   GenericViewSet):
    """
    Model view set for model MasterExperience
    """

    serializer_class = MasterExperienceModelSerializer
    queryset = MasterExperience.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerMasterExperiencePermission,)

    def perform_create(self, serializer: MasterExperienceModelSerializer):
        serializer.validated_data['master'] = self.request.user.master
        serializer.save()


class MasterModelViewSet(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    """
    Model View Set for model master
    """

    queryset = Master.objects.all()
    serializer_class = MasterModelSerializer
    permission_classes = (IsOwnerMasterPermission,)

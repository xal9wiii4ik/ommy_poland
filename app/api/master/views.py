import typing as tp

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, mixins

from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from api.master.models import Master
from api.master.permissions import IsOwnerMasterPermission
from api.master.serializers import MasterModelSerializer, MasterRegisterSerializer
from api.master.services import create_master_account


class RegisterMasterApiView(APIView):
    """
    View for register new master
    """

    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=MasterRegisterSerializer)
    def post(self, request: Request, *args: tp.Any, **kwargs: tp.Any) -> Response:
        serializer = MasterRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer_data = serializer.data

        user_pk = create_master_account(data=serializer_data, master_experiences=request.data.get('master_experience'))
        serializer_data.update({'user_pk': user_pk})
        return Response(data=serializer_data, status=status.HTTP_201_CREATED)


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

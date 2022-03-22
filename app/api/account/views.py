import typing as tp

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema

from api.account.serializers import UserRegisterSerializer
from api.account.services import create_user_account


class RegisterUserApiView(APIView):
    """
    View for register new user
    """

    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=UserRegisterSerializer)
    def post(self, request: Request, *args: tp.Any, **kwargs: tp.Any) -> Response:
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer_data = serializer.data

        create_user_account(data=serializer_data)
        return Response(data=serializer_data, status=status.HTTP_201_CREATED)

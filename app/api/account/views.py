import typing as tp

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema

from api.account.serializers import (
    UserRegisterSerializer,
    ForgotPasswordSerializer,
    UpdatePasswordSerializer
)
from api.account.services import create_user_account, update_account_password
from api.authenticate.serializers import CustomTokenObtainPairSerializer
from api.authenticate.tasks.activate_user.tasks import send_phone_activate_message
from api.utils.services import get_serializer_data, set_refresh_to_cookie


class RegisterUserApiView(APIView):
    """
    View for register new user
    """

    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=UserRegisterSerializer)
    def post(self, request: Request, *args: tp.Any, **kwargs: tp.Any) -> Response:
        serializer_data = get_serializer_data(data=request.data, serializer=UserRegisterSerializer)
        create_user_account(data=serializer_data)
        return Response(data=serializer_data, status=status.HTTP_201_CREATED)


class ForgotPasswordApiView(APIView):
    """
    View for update user password
    """

    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=ForgotPasswordSerializer)
    def post(self, request: Request, *args: tp.Any, **kwargs: tp.Any) -> Response:
        serializer_data = get_serializer_data(data=request.data, serializer=ForgotPasswordSerializer)
        send_phone_activate_message.delay(serializer_data['user_pk'])
        return Response(data={'success': 'Код активации был отправлен'}, status=status.HTTP_200_OK)


class UpdatePasswordApiView(APIView):
    """
    View for update password after confirm code
    """

    @swagger_auto_schema(request_body=UpdatePasswordSerializer)
    def post(self, request: Request, *args: tp.Any, **kwargs: tp.Any) -> Response:
        serializer_data = get_serializer_data(data=request.data, serializer=UpdatePasswordSerializer)
        user = update_account_password(data=serializer_data)

        # getting tokens for user
        # not in get_serializer_data because validated_data is used in this case
        token_serializer = CustomTokenObtainPairSerializer(
            data={
                'password': serializer_data['repeat_password'],
                'username': user.username
            }
        )
        token_serializer.is_valid(raise_exception=True)
        token_serializer_data = token_serializer.validated_data
        return Response(data=token_serializer_data, status=status.HTTP_200_OK)

    def finalize_response(self, request: Request, response: Response, *args, **kwargs):
        set_refresh_to_cookie(response=response)
        return super().finalize_response(request, response, *args, **kwargs)

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
from ommy_polland import settings


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


class ForgotPasswordApiView(APIView):
    """
    View for update user password
    """

    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=ForgotPasswordSerializer)
    def post(self, request: Request, *args: tp.Any, **kwargs: tp.Any) -> Response:
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer_data = serializer.data
        send_phone_activate_message.delay(serializer_data['user_pk'])
        return Response(data={'success': 'Код активации был отправлен'}, status=status.HTTP_200_OK)


class UpdatePasswordApiView(APIView):
    """
    View for update password after confirm code
    """

    @swagger_auto_schema(request_body=UpdatePasswordSerializer)
    def post(self, request: Request, *args: tp.Any, **kwargs: tp.Any) -> Response:
        serializer = UpdatePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer_data = serializer.data
        user = update_account_password(data=serializer_data)
        print(user.username)
        username = user.username
        data = {
            'password': serializer_data['repeat_password'],
            'username': username
        }
        print(data)
        token_serializer = CustomTokenObtainPairSerializer(
            data={
                'password': serializer_data['repeat_password'],
                'username': username
            }
        )
        token_serializer.is_valid(raise_exception=True)
        token_serializer_data = token_serializer.validated_data
        return Response(data=token_serializer_data, status=status.HTTP_200_OK)

    def finalize_response(self, request: Request, response: Response, *args, **kwargs):
        if response.data.get('refresh'):
            cookie_max_age = 60 * settings.REFRESH_TOKEN_LIFETIME
            response.set_cookie('refresh', response.data['refresh'], max_age=cookie_max_age, httponly=True,
                                samesite='None', secure=True)
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)

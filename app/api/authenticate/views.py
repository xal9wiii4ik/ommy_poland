import typing as tp

from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.authenticate.serializers import (
    CustomTokenObtainPairSerializer,
    ActivateAccountSerializer,
    CookieTokenRefreshSerializer,
    CheckActivationCodeSerializer, CustomTokenObtainPairActivateSerializer,
)
from api.authenticate.services import activate_account
from api.utils.services import get_serializer_data, set_refresh_to_cookie


class CookieTokenObtainPairView(TokenObtainPairView):
    """
    Custom view for setting token to cookie
    """

    serializer_class = CustomTokenObtainPairSerializer

    def finalize_response(self, request: Request, response: Response, *args, **kwargs):
        set_refresh_to_cookie(response=response)
        return super().finalize_response(request, response, *args, **kwargs)


class CookieTokenRefreshView(TokenRefreshView):
    """
    Custom view for refresh token using cookie
    """

    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request: Request, response: Response, *args, **kwargs):
        set_refresh_to_cookie(response=response)
        return super().finalize_response(request, response, *args, **kwargs)


class ActivateAccountApiView(APIView):
    """
    Api view for activating account
    """

    @swagger_auto_schema(request_body=ActivateAccountSerializer)
    def post(self, request: Request, *args: tp.Any, **kwargs: tp.Any) -> Response:
        serializer_data = get_serializer_data(data=request.data, serializer=ActivateAccountSerializer)

        is_activated = activate_account(data=serializer_data)

        if is_activated:
            token_serializer = CustomTokenObtainPairActivateSerializer(
                data={
                    'phone_number': is_activated,
                    'password': 'hard',
                }
            )
            token_serializer.is_valid(raise_exception=False)
            token_serializer_data = token_serializer.validated_data
            return Response(data=token_serializer_data, status=status.HTTP_200_OK)
        return Response(data={'error': 'Account with this id and code does not exist'},
                        status=status.HTTP_400_BAD_REQUEST)

    def finalize_response(self, request: Request, response: Response, *args, **kwargs):
        set_refresh_to_cookie(response=response)
        return super().finalize_response(request, response, *args, **kwargs)


class CheckActivationCode(APIView):
    """
    Check activation code(if he exist in db)
    """

    @swagger_auto_schema(request_body=CheckActivationCodeSerializer)
    def post(self, request: Request, *args: tp.Any, **kwargs: tp.Any) -> Response:
        serializer_data = get_serializer_data(data=request.data, serializer=CheckActivationCodeSerializer)
        return Response(data=serializer_data, status=status.HTTP_200_OK)

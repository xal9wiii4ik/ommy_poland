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
)
from api.authenticate.services import activate_account

from ommy_polland import settings


class CookieTokenObtainPairView(TokenObtainPairView):
    """
    Custom view for setting token to cookie
    """

    serializer_class = CustomTokenObtainPairSerializer

    def finalize_response(self, request, response: Response, *args, **kwargs):
        if response.data.get('refresh'):
            cookie_max_age = 3600 * settings.REFRESH_TOKEN_LIFETIME
            response.set_cookie('refresh', response.data['refresh'], max_age=cookie_max_age, httponly=True,
                                domain='localhost')
            del response.data['refresh']
            print(response.cookies)
        return super().finalize_response(request, response, *args, **kwargs)


class CookieTokenRefreshView(TokenRefreshView):
    """
    Custom view for refresh token using cookie
    """

    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request: Request, response, *args, **kwargs):
        print(request.COOKIES)
        if response.data.get('refresh'):
            cookie_max_age = 3600 * settings.REFRESH_TOKEN_LIFETIME
            response.set_cookie('refresh', response.data['refresh'], max_age=cookie_max_age, httponly=True,
                                domain='localhost')
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)


class ActivateAccountApiView(APIView):
    """
    Api view for activating account
    """

    @swagger_auto_schema(request_body=ActivateAccountSerializer)
    def post(self, request: Request, *args: tp.Any, **kwargs: tp.Any) -> Response:
        serializer = ActivateAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer_data = serializer.data

        is_activated = activate_account(data=serializer_data)
        if is_activated:
            return Response(data={'success': 'Account has been activated'}, status=status.HTTP_200_OK)
        return Response(data={'error': 'Account with this id and code does not exist'},
                        status=status.HTTP_400_BAD_REQUEST)

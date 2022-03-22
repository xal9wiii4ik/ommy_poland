import typing as tp

from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from api.authenticate.serializers import CustomTokenObtainPairSerializer, ActivateAccountSerializer
from api.authenticate.services import activate_account


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view for token
    """

    serializer_class = CustomTokenObtainPairSerializer


class ActivateAccountApiView(APIView):
    """
    Api view for activating account
    """

    @swagger_auto_schema(request_body=ActivateAccountSerializer)
    def post(self, request: Request, *args: tp.Any, **kwargs: tp.Any) -> Response:
        serializer = ActivateAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer_data = serializer.data

        is_exist = activate_account(data=serializer_data)
        if is_exist:
            return Response(data={'success': 'Account has been activated'}, status=status.HTTP_200_OK)
        return Response(data={'error': 'Account with this id and code does not exist'},
                        status=status.HTTP_400_BAD_REQUEST)

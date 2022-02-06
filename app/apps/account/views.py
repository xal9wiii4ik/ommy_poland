import typing as tp

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth import get_user_model

from drf_yasg.utils import swagger_auto_schema

from apps.account.serializers import UserRegisterSerializer, CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view for token
    """

    serializer_class = CustomTokenObtainPairSerializer


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
        del serializer_data['repeat_password']
        user = get_user_model().objects.create(**serializer_data)
        del serializer_data['password']
        serializer_data['id'] = user.id
        return Response(data=serializer_data, status=status.HTTP_200_OK)

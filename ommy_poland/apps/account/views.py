import typing as tp

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class RegisterUserApiView(APIView):
    """
    View for register new user
    """

    permission_classes = (AllowAny,)

    def post(self, request: Request, *args: tp.Any, **kwargs: tp.Any) -> Response:
        # TODO add registration
        # get_user_model() => get current user model
        return Response(data={}, status=status.HTTP_200_OK)

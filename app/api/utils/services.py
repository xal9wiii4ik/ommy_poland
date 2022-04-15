import typing as tp

from rest_framework.response import Response
from rest_framework.serializers import SerializerMetaclass

from ommy_polland import settings


def get_serializer_data(data: tp.Dict[str, tp.Any], serializer: SerializerMetaclass) -> tp.Dict[str, tp.Any]:
    """
    Get data from serializer
    Args:
        serializer: current serializer for view
        data: data from request
    Returns:
        data from serializer
    """

    serializer = serializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer_data = serializer.data
    return serializer_data


def set_refresh_to_cookie(response: Response):
    """
    Set refresh token to cookie
    Args:
        response: current response
    """

    if response.data.get('refresh'):
        cookie_max_age = 60 * settings.REFRESH_TOKEN_LIFETIME
        response.set_cookie('refresh', response.data['refresh'], max_age=cookie_max_age, httponly=True,
                            samesite='None', secure=True)
        del response.data['refresh']

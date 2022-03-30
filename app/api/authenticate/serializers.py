import typing as tp

from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from ommy_polland import settings


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    """
    Custom serializer for refresh token
    """

    refresh = None

    def validate(self, attrs):
        print(self.context['request'].COOKIES)
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh')
        print(attrs)
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise InvalidToken('No valid refresh token found in cookie')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """ Custom token serializer """

    def validate(self, attrs: tp.Any) -> tp.Any:
        """ add fields to response data """

        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)

        user = get_user_model().objects.get(username=attrs['username'])
        data['fullname'] = f'{user.first_name} {user.last_name}'

        data.update({
            'expires_in': settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            'refresh_life_time': settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
        })
        return data


class ActivateAccountSerializer(serializers.Serializer):
    """
    Serializer for activate account
    """

    user_pk = serializers.IntegerField(required=True)
    code = serializers.IntegerField(min_value=100000, max_value=999999)

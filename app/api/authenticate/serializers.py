import typing as tp

from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from api.authenticate.models import ActivateAccountCode


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    """ Custom serializer for refresh token """

    refresh = None

    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise InvalidToken('No valid refresh token found in cookie')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """ Custom token serializer """

    def validate(self, attrs: tp.Any) -> tp.Any:
        """ add fields to response data """

        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)

        # user = get_user_model().objects.get(username=attrs['username'])
        data['fullname'] = f'{self.user.first_name} {self.user.last_name}'
        return data


class CustomTokenObtainPairActivateSerializer(TokenObtainPairSerializer):
    """ Custom token serializer """

    def validate(self, attrs: tp.Any) -> tp.Any:
        """ add fields to response data """

        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'password': attrs['password'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = get_user_model().objects.get(username=attrs['username'])
        refresh = self.get_token(self.user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

        return data


class CheckActivationCodeSerializer(serializers.Serializer):
    """ Serializer for checking activation code(if he exist in db) """

    code = serializers.IntegerField(min_value=1000, max_value=9999)

    @staticmethod
    def validate_code(code: int) -> int:
        is_exist = ActivateAccountCode.objects.filter(code=code).exists()
        if not is_exist:
            raise ValidationError('Не верный код активации')
        return code


class ActivateAccountSerializer(CheckActivationCodeSerializer):
    """ Serializer for activate account """

    user_pk = serializers.IntegerField(required=True)

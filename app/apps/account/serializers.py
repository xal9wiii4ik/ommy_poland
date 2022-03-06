import typing as tp

from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from ommy_polland import settings


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


class UserRegisterSerializer(serializers.Serializer):
    """
    Serializer for register new user
    """

    username = serializers.CharField(max_length=50, required=False, read_only=True)
    email = serializers.EmailField(max_length=100, required=False)
    phone_number = serializers.CharField(max_length=13, required=True)
    first_name = serializers.CharField(max_length=100, required=True)
    last_name = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, required=True)
    repeat_password = serializers.CharField(max_length=100, required=True)

    @staticmethod
    def validate_phone_number(value: str) -> str:
        """
        Validate phone_number
        Args:
            value: value
        Raise:
            exception if invalid field
        Returns:
             value
        """

        if value.find('+') == 0 and value.replace('+', '').isdigit() and len(value) == 13:
            if get_user_model().objects.filter(phone_number=value):
                raise serializers.ValidationError({'User with this phone number already exist'})
            return value
        else:
            raise serializers.ValidationError({'Invalid phone number, example: +375*********'})

    @staticmethod
    def validate_email(value: str) -> str:
        """
        Validate email using django default email validator
        Args:
            value: value
        Raise:
            exception if invalid field
        Returns:
             value
        """

        if value is not None:
            validate_email(value=value)
            accounts = get_user_model().objects.filter(email=value)
            if accounts:
                raise serializers.ValidationError({'User with this email already exist'})
        return value

    @staticmethod
    def validate_password(value: str) -> str:
        """
        Validate password using django default password validator
        Args:
            value: value
        Raise:
            exception if invalid field
        Returns:
             value
        """

        password_validation.validate_password(password=value)
        return value

    def validate(self, attrs: tp.Dict[str, tp.Any]) -> tp.Dict[str, tp.Any]:
        """
        Validate all fields
        Args:
            attrs: OrderedDict with values
        Raise:
            exception if invalid fields
        Returns:
            attrs
        """

        if attrs.get('password') != attrs.get('repeat_password'):
            raise serializers.ValidationError({'repeat_password': 'Repeat password should be equal to password'})
        attrs['password'] = make_password(password=attrs['password'])
        attrs['username'] = attrs.get('phone_number')
        return attrs

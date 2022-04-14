import typing as tp

from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.authenticate.models import ActivateAccountCode


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
    def validate_phone_number(phone_number: str) -> str:
        if phone_number.find('+') == 0 and phone_number.replace('+', '').isdigit() and len(phone_number) == 13:
            if get_user_model().objects.filter(phone_number=phone_number):
                raise serializers.ValidationError({'User with this phone number already exist'})
            return phone_number
        else:
            raise serializers.ValidationError({'Invalid phone number, example: +375*********'})

    @staticmethod
    def validate_email(email: str) -> str:
        if email is not None:
            validate_email(value=email)
            accounts = get_user_model().objects.filter(email=email)
            if accounts:
                raise serializers.ValidationError({'User with this email already exist'})
        return email

    @staticmethod
    def validate_password(password: str) -> str:
        password_validation.validate_password(password=password)
        return password

    def validate(self, attrs: tp.Dict[str, tp.Any]) -> tp.Dict[str, tp.Any]:
        if attrs.get('password') != attrs.get('repeat_password'):
            raise serializers.ValidationError({'repeat_password': 'Repeat password should be equal to password'})
        attrs['password'] = make_password(password=attrs['password'])
        attrs['username'] = attrs.get('phone_number')
        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    """
    Serializer for forgot password
    """

    phone_number = serializers.CharField(max_length=13, required=True)
    user_pk = serializers.IntegerField(read_only=True)

    @staticmethod
    def validate_phone_number(phone_number: str) -> str:
        if phone_number.find('+') == 0 and phone_number.replace('+', '').isdigit() and len(phone_number) == 13:
            if get_user_model().objects.filter(phone_number=phone_number):
                return phone_number
            raise serializers.ValidationError('Пользователь с таким номером телефоне не найден в нашей базе')
        else:
            raise serializers.ValidationError('Неверный номер телефона, прмиер: +375*********')

    def validate(self, attrs: tp.Dict[str, tp.Any]) -> tp.Dict[str, tp.Any]:
        user = get_user_model().objects.filter(phone_number=attrs['phone_number'])
        if not user:
            raise serializers.ValidationError('Пользователь с таким номером телефоне не найден в нашей базе')

        attrs['user_pk'] = user[0].pk
        return attrs


class UpdatePasswordSerializer(serializers.Serializer):
    """
    Update password serializer
    """

    password = serializers.CharField(max_length=100, required=True)
    repeat_password = serializers.CharField(max_length=100, required=True)
    code = serializers.IntegerField(min_value=1000, max_value=9999)
    user_pk = serializers.IntegerField(read_only=True)

    @staticmethod
    def validate_password(password: str) -> str:
        password_validation.validate_password(password=password)
        return password

    def validate(self, attrs: tp.Dict[str, tp.Any]) -> tp.Dict[str, tp.Any]:
        activation_code = ActivateAccountCode.objects.filter(code=attrs['code'])
        if not activation_code:
            raise ValidationError('Не верный код активации')
        attrs['user_pk'] = activation_code[0].user.pk

        if attrs.get('password') != attrs.get('repeat_password'):
            raise serializers.ValidationError({'repeat_password': 'Repeat password should be equal to password'})
        attrs['password'] = make_password(password=attrs['password'])
        return attrs

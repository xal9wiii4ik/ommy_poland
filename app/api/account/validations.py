import re

from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from django.contrib.auth import password_validation


def password_validate(password: str) -> str:
    """
    Validate password
    """

    regular_expression = r'^[A-Za-z0-9_]*$'
    if re.search(regular_expression, password):
        password_validation.validate_password(password=password)
        return password
    else:
        raise serializers.ValidationError('Пароль должен содержать латинские буквы и цыфры')


def repeat_password_validate(password: str, repeat_password: str) -> str:
    """
    Validate repeat password
    Return:
        hash password
    """

    if password != repeat_password:
        raise serializers.ValidationError({'repeat_password': 'repeat_password должен быть равен password'})
    return make_password(password=password)

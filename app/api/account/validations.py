import re

from django.contrib.auth.hashers import make_password
from rest_framework import serializers


def password_validate(password: str) -> str:
    """
    Validate password
    """

    regular_expression = r'^[A-Za-z0-9_]*$'
    if re.search(regular_expression, password) and len(password) >= 8:
        return password
    else:
        raise serializers.ValidationError(
            'Пароль должен содержать латинские буквы и цыфры и содержать 8 и больше симовлов'
        )


def repeat_password_validate(password: str, repeat_password: str) -> str:
    """
    Validate repeat password
    Return:
        hash password
    """

    if password != repeat_password:
        raise serializers.ValidationError({'repeat_password': 'repeat_password должен быть равен password'})
    return make_password(password=password)

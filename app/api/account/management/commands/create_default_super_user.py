import logging
import typing as tp

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from ommy_polland import settings


class Command(BaseCommand):
    """
    Create default super user
    """

    help = 'Create default super user'

    def handle(self, *args: tp.Any, **options: tp.Any) -> None:
        logging.info('Start creating default super user')

        is_exist = get_user_model().objects.filter(phone_number=settings.DEFAULT_SUPER_USER_USERNAME,
                                                   email=settings.DEFAULT_SUPER_USER_EMAIL).exists()
        if not is_exist:
            get_user_model().objects.create(phone_number=settings.DEFAULT_SUPER_USER_USERNAME,
                                            password=make_password(settings.DEFAULT_SUPER_USER_PASSWORD),
                                            email=settings.DEFAULT_SUPER_USER_EMAIL,
                                            is_staff=True,
                                            is_superuser=True,
                                            is_active=True)

        logging.info('Super user has been created')

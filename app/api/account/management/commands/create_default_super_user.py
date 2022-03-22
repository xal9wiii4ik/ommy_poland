import logging
import typing as tp

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

        is_exist = get_user_model().objects.filter(username=settings.DEFAULT_SUPER_USER_USERNAME,
                                                   email=settings.DEFAULT_SUPER_USER_EMAIL).exists()
        if not is_exist:
            get_user_model().objects.create_superuser(username=settings.DEFAULT_SUPER_USER_USERNAME,
                                                      password=settings.DEFAULT_SUPER_USER_PASSWORD,
                                                      email=settings.DEFAULT_SUPER_USER_EMAIL)

        logging.info('Super user has been created')

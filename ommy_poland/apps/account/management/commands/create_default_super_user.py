import logging
import typing as tp

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from ommy_polland import settings


class Command(BaseCommand):
    """
    Create default super user
    """

    help = 'Create default super user'

    def handle(self, *args: tp.Any, **options: tp.Any) -> None:
        logging.info('Start creating default super user')

        try:
            get_user_model().objects.create_superuser(username=settings.DEFAULT_SUPER_USER_USERNAME,
                                                      password=settings.DEFAULT_SUPER_USER_PASSWORD,
                                                      email=settings.DEFAULT_SUPER_USER_EMAIL)
        except IntegrityError:
            logging.info('Default super user already exist in db')
        except Exception as e:
            logging.warning(f'Something was wrong in create_default_super_user {e}')

        logging.info('Super user has been created')

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Model for user account
    """

    class Meta:
        abstract = False
        verbose_name = 'Client'

    phone_number = models.CharField(verbose_name='Phone Number', max_length=13, unique=True)
    address = models.CharField(verbose_name='address',
                               max_length=100,
                               null=True,
                               blank=True)
    is_master = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'pk: {self.pk}, username: {self.username}, email: {self.email}, ' \
               f'phone_number: {self.phone_number}'

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Model for user account
    """

    class Meta:
        abstract = False
        verbose_name = 'Client'

    USERNAME_FIELD = 'phone_number'
    username = None

    middle_name = models.CharField(max_length=150, verbose_name='middle name', null=True, blank=True)
    phone_number = models.CharField(verbose_name='Phone Number', max_length=13, unique=True)
    address = models.CharField(verbose_name='Master address',
                               max_length=100,
                               null=True,
                               blank=True)
    is_master = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'id: {self.pk} phone_number: {self.phone_number}'

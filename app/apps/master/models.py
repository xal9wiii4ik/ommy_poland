from django.db import models

from apps.account.models import User


class Master(User):
    """
    Model for table user
    """

    class Meta:
        db_table = 'master'

    work_experience = models.PositiveIntegerField(verbose_name='work experience')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='longitude in degrees')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='latitude in degrees')

    def __str__(self) -> str:
        return f'pk: {self.pk}, first_name: {self.first_name}, last_name: {self.last_name}'

from django.contrib.auth import get_user_model
from django.db import models


class Master(models.Model):
    """
    Model for table user
    """

    user = models.OneToOneField(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='master',
        verbose_name='user'
    )
    work_experience = models.PositiveIntegerField(verbose_name='work experience')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='longitude in degrees')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='latitude in degrees')
    city = models.CharField(max_length=100, verbose_name='city')

    def __str__(self) -> str:
        return f'pk: {self.pk}, first_name: {self.user.first_name}, last_name: {self.user.last_name}, city: {self.city}'

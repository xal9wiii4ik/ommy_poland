from django.contrib.auth import get_user_model
from django.db import models


class WorkSphere(models.Model):
    """
    Model for table work sphere
    """

    name = models.CharField(max_length=50, verbose_name='work sphere name')

    def __str__(self) -> str:
        return f'pk: {self.pk}, name: {self.name}'


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
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='longitude in degrees')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='latitude in degrees')
    city = models.CharField(max_length=100, verbose_name='city')

    def __str__(self) -> str:
        return f'id: {self.pk}, city: {self.city}'


class MasterExperience(models.Model):
    """
    Model for table master experience
    """

    work_sphere = models.ForeignKey(
        to=WorkSphere,
        on_delete=models.CASCADE,
        verbose_name='Work Sphere',
        related_name='work_sphere'
    )
    experience = models.PositiveIntegerField(verbose_name='experience')
    master = models.ForeignKey(
        to=Master,
        on_delete=models.CASCADE,
        verbose_name='Master',
        related_name='master_experience'
    )

    def __str__(self) -> str:
        return f'pk: {self.pk}, work sphere: {self.work_sphere},' \
               f' experience: {self.experience}, master_pk: {self.master.pk}'

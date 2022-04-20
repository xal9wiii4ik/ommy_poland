import fleep

from enum import Enum

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models

from api.master.models import Master, WorkSphere


def get_file_type(file_bytes: bytes) -> str:
    """
    Get file type from file
    Args:
        file_bytes: bytes of file
    Returns:
        file type
    """

    file_info = fleep.get(file_bytes)
    if not any(file_info.type):
        raise Exception
    file_type = file_info.type[0]
    return file_type


class OrderStatus(Enum):
    """
    Enums with order statuses
    """

    OPEN = 'open'
    ACCEPTED = 'accepted'
    IN_PROGRESS = 'in_progress'
    DONE = 'done'
    PAID = 'paid'
    CANCELED = 'canceled'


class Order(models.Model):
    """
    Model for table order
    """

    work_sphere = models.ForeignKey(to=WorkSphere,
                                    on_delete=models.SET_NULL,
                                    verbose_name='order work sphere',
                                    related_name='order_work_sphere',
                                    null=True,
                                    blank=True)
    customer = models.ForeignKey(to=get_user_model(),
                                 on_delete=models.SET_NULL,
                                 related_name='order_customer',
                                 null=True,
                                 blank=True)
    name = models.CharField(max_length=50, verbose_name='Name of order', null=True, blank=True)
    number_employees = models.IntegerField(verbose_name='number of employees')
    desired_time_end_work = models.CharField(max_length=10, verbose_name='desired time end of work')
    start_time = models.DateTimeField(verbose_name='work start time')
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                verbose_name='Order price',
                                default=0,
                                null=True,
                                blank=True)
    description = models.TextField(max_length=1024, verbose_name='Description of order', null=True, blank=True)
    address = models.CharField(max_length=128, verbose_name='Address of the customer', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=30,
        choices=[(order_status.name, order_status.value) for order_status in OrderStatus],
        default=OrderStatus.OPEN.value
    )
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='longitude in degrees')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='latitude in degrees')
    types_of_work = ArrayField(
        models.CharField(max_length=200),
        null=True,
        blank=True,
        verbose_name='types of work'
    )
    city = models.CharField(max_length=100, verbose_name='city of the order')
    master = models.ManyToManyField(
        to=Master,
        blank=True,
        related_name='order_master',
        verbose_name='Order master'
    )

    def __str__(self) -> str:
        return f'pk: {self.pk}, name: {self.name}, address: {self.address}, ' \
               f'date_created: {self.date_created}, ' \
               f'status: {self.status}, work_sphere: {self.work_sphere}'


class OrderFile(models.Model):
    """
    Database table order files for order
    """

    class Meta:
        db_table = 'order_file'

    order = models.ForeignKey(to=Order,
                              on_delete=models.CASCADE,
                              verbose_name='Order',
                              related_name='order_files')
    bucket_path = models.CharField(max_length=1056, verbose_name='Bucket path')

    def __str__(self) -> str:
        return f'pk: {self.pk}, order_id: {self.order.pk}, ' \
               f'order_name: {self.order.name}, bucket_path: {self.bucket_path}'

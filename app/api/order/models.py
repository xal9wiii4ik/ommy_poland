import fleep

from enum import Enum

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models

from api.master.models import Master, WorkSphere
from api.order.models_validators import validate_less_then_forty


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

    SEARCH_MASTER = 'Поиск мастера'
    AWAIT_EXECUTING = 'Ожидает выполнения'
    CANCELED = 'Заявка отменена'
    PAID = 'Оплачено'


class Order(models.Model):
    """
    Model for table order
    """

    class Meta:
        verbose_name = 'Order'

    work_sphere = models.ForeignKey(to=WorkSphere,
                                    on_delete=models.SET_NULL,
                                    verbose_name='order work sphere',
                                    related_name='order_work_sphere',
                                    null=True)
    customer = models.ForeignKey(to=get_user_model(),
                                 on_delete=models.SET_NULL,
                                 related_name='order_customer',
                                 null=True)
    name = models.CharField(max_length=50, verbose_name='Order name')
    number_employees = models.PositiveIntegerField(
        validators=[validate_less_then_forty],
        verbose_name='number of employees'
    )
    desired_time_end_work = models.CharField(max_length=40, verbose_name='Work duration')
    start_time = models.DateTimeField(verbose_name='work start time')
    price = models.DecimalField(max_digits=8,
                                decimal_places=2,
                                verbose_name='Order price')
    description = models.TextField(max_length=255, verbose_name='Description of order', null=True, blank=True)
    address = models.CharField(max_length=256, verbose_name='Address of the customer', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=30,
        choices=[(order_status.name, order_status.value) for order_status in OrderStatus],
        default=OrderStatus.SEARCH_MASTER.name
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
        verbose_name = 'Order File'

    order = models.ForeignKey(to=Order,
                              on_delete=models.CASCADE,
                              verbose_name='Order',
                              related_name='order_files')
    bucket_path = models.CharField(max_length=1056, verbose_name='Bucket path')

    def __str__(self) -> str:
        return f'pk: {self.pk}, order_id: {self.order.pk}, ' \
               f'order_name: {self.order.name}, bucket_path: {self.bucket_path}'

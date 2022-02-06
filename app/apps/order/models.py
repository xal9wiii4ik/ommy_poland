import logging
import os
from enum import Enum

import fleep

from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


def create_unique_file_url(file_name: str) -> str:
    """
    Creating unique image_url
    Args:
         file_name: name of file
    Returns:
        str: new path to save the image
    """

    new_directory = timezone.now()
    new_directory = datetime.strftime(new_directory, '%Y-%m-%dT%H:%M:%S.%f%z')
    new_path = new_directory + '/' + file_name
    return os.path.join(new_path)


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


class WorkSphere(models.Model):
    """
    Model for table work sphere
    """

    name = models.CharField(max_length=100, verbose_name='work sphere')

    def __str__(self) -> str:
        return f'pk: {self.pk}, name: {self.name}'


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
    start_time = models.DateTimeField(verbose_name='work start time', null=True, blank=True)
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

    file = models.FileField(upload_to='', verbose_name='Order File')
    order = models.ForeignKey(to=Order,
                              on_delete=models.CASCADE,
                              verbose_name='Order',
                              related_name='order_files')
    file_type = models.CharField(max_length=100,
                                 verbose_name='File type',
                                 null=True,
                                 blank=True)

    def save(self, *args, **kwargs):
        if self.file:
            try:
                self.file.name = create_unique_file_url(file_name=self.file.name)
                if self.file_type is None:
                    self.file_type = get_file_type(file_bytes=self.file.read())
            except IndexError:
                logging.warning(f'Un read bytes for file for order {self.order.pk}')
            else:
                return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'pk: {self.pk}, order_id: {self.order.pk}, order_name: {self.order.name}, file_type: {self.file_type}'

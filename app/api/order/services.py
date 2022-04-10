import typing as tp
import logging
import boto3
import fleep

from math import radians, cos, sin, sqrt, asin

from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from rest_framework.request import Request

from api.master.models import Master
from api.order.permissions import IsCustomerPermission
from api.order.tasks.order_notification.tasks import (
    send_notification_with_new_order_to_masters,
    send_masters_info_to_customer,
    send_masters_notification_with_cancel_order,
)
from api.order.models import Order, OrderFile, OrderStatus
from api.telegram_bot.tasks.notifications.tasks import send_cancel_order_to_order_chat
from api.utils.search_masters.eval import MasterComplianceAssessment

from ommy_polland.settings import ORDER_BUCKET, BUCKET_REGION


def calculate_distance(order_longitude: float,
                       order_latitude: float,
                       master_longitude: float,
                       master_latitude: float) -> float:
    """
    Calculate distance between master and order location
    Args:
        order_longitude: order longitude in degrees
        order_latitude: order latitude in degrees
        master_longitude: master longitude in degrees
        master_latitude: master latitude in degrees
    Return:
        distance in kilometers
    """

    # convert decimal degrees to radians
    order_longitude, order_latitude, master_longitude, master_latitude = map(
        radians,
        [order_longitude, order_latitude, master_longitude, master_latitude]
    )
    # haversine formula
    distance_longitude = master_latitude - order_longitude
    distance_latitude = master_latitude - order_latitude
    intermediate_value = sin(
        distance_latitude / 2
    ) ** 2 + cos(order_latitude) * cos(master_latitude) * sin(distance_longitude / 2) ** 2

    distance = 2 * asin(sqrt(intermediate_value))
    # Radius of earth in kilometers is 6371
    distance_kilometers = 6371000 * distance
    return distance_kilometers


def master_exist_in_city(city: str) -> QuerySet:
    """
    Check if master exist in order city
    Args:
        city: order city
    Returns:
        True if master exist
        QuerySet if exist
    """

    masters = Master.objects.filter(city=city.lower())
    return masters


def generate_masters_queue(data: tp.List[tp.List[tp.Union[int, float]]], masters: QuerySet) -> tp.List[str]:
    """
    Generate masters queue
    Args:
        data: a list with the data needed to generate the probability of the master
        masters: Queryset with masters
    Returns:
        sorted masters phone numbers
    """

    # get masters probabilities
    model = MasterComplianceAssessment()
    masters_probabilities = model.get_masters_probabilities(data)

    # creating a queue of masters and getting sort list with phone numbers
    masters_phone_numbers = [master.user.phone_number for master in masters]
    masters_queue = list(zip(masters_phone_numbers, masters_probabilities))
    sorted_masters_queue = sorted(masters_queue, key=lambda x: x[1], reverse=True)
    sort_masters_phone_numbers = [masters_queue_item[0] for masters_queue_item in sorted_masters_queue]
    return sort_masters_phone_numbers


def find_order_masters(order_pk: int,
                       order_longitude: float,
                       order_latitude: float,
                       masters: QuerySet) -> tp.Dict[str, str]:
    """
    Find masters for order
    Args:
        order_pk: current order pk
        order_longitude: order longitude
        order_latitude: order latitude
        masters: queryset with masters
    Returns:
        dict with success message
    """

    data = []

    for master in masters:
        data.append(
            [1, calculate_distance(
                order_longitude=order_longitude,
                order_latitude=order_latitude,
                master_longitude=master.longitude,
                master_latitude=master.latitude
            ), master.work_experience, 1, 1, 1, 1, 1.6]
        )

    sort_masters_phone_numbers = generate_masters_queue(data=data, masters=masters)

    start_time = timezone.now()
    send_notification_with_new_order_to_masters.delay(order_pk, sort_masters_phone_numbers, start_time)
    return {'success': f'Мы нашли {len(sort_masters_phone_numbers)} подходящих мастеров для вашего'}


def create_order_files(order: Order, files: tp.List[tp.IO]) -> None:
    """ Func for saving pictures in database
    Args:
        order: post id
        files: list with files
    """

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(ORDER_BUCKET)
    order_id = order.pk

    for file in files:
        file_bytes = file.read()
        try:
            file_info = fleep.get(file_bytes)
        except TypeError:
            logging.warning(msg=f'Not file for order: {order_id}')
            continue

        if not file_info.mime:
            logging.warning(msg=f'Something was wrong with file for order: {order_id}')
            continue

        file_path = f'{order_id}/{file.name}'
        file = bucket.put_object(Key=file_path,
                                 Body=file_bytes)
        bucket_path = f'https://s3-{BUCKET_REGION}.amazonaws.com/{ORDER_BUCKET}/{file.key}'  # type: ignore
        OrderFile.objects.create(order=order, bucket_path=bucket_path)


def get_order_or_404(order_pk: int) -> tp.Union[Order, int]:
    """
    Get order or 404
    Args:
        order_pk: order pk
    Returns:
        Order object or error message
    """

    try:
        order = Order.objects.get(pk=order_pk)
        return order
    except Order.DoesNotExist:
        return 404


def add_master_to_order(order: Order, user: get_user_model) -> tp.Tuple[str, int]:
    """
    Add master to order
    Args:
        order: Order object
        user: current user
    Returns:
        response message, response status
    """

    order_pk = order.pk

    if order.number_employees <= order.master.all().count():
        return 'Мы уже нашли достаточное кол-во мастеров для этого заказа', 400
    order.master.add(user.master)

    if order.status == 'CANCELED':
        return 'К сожелению заказ был отменен, ожидайте остальные заказы', 400

    if order.number_employees == order.master.all().count():
        send_masters_info_to_customer.delay(order_pk)

    order.status = OrderStatus.ACCEPTED.name
    order.save()
    return 'Вы приняли заказ, подробности заказа: тут подробности', 200


def cancel_order(order: Order, request: Request, view_name: str) -> tp.Tuple[tp.Dict[str, str], int]:
    """
    Cancel order
    Args:
        order: Order
        request: Request
        view_name: view name
    Returns:
        response dict, response status
    """

    permission_class = IsCustomerPermission()
    has_object_permission = permission_class.has_object_permission(
        request=request,
        view=view_name,
        obj=order
    )
    if has_object_permission:
        order.status = 'CANCELED'
        order.save()

        send_masters_notification_with_cancel_order.delay(order.pk)
        send_cancel_order_to_order_chat.delay(order.pk)

        return {'order': 'Заказ был отменен'}, 200
    else:
        return {'detail': 'You do not have permission to perform this action.'}, 403

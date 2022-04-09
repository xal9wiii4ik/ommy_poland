import typing as tp

from datetime import timedelta, datetime
from twilio.rest import Client

from celery import shared_task

from ommy_polland import settings


# TODO add link, update commisiya
@shared_task
def send_notification_with_new_order_to_masters(order_pk: int,
                                                masters_phone_numbers: tp.List[str],
                                                current_time: str) -> None:
    """
    Send notification with new order to masters
    Args:
        order_pk: order pk
        masters_phone_numbers: masters phone numbers
        current_time: current_time
    """

    from api.order.models import Order

    order = Order.objects.get(pk=order_pk)
    if order.master is None:
        wait_time = datetime.strptime(current_time, '%Y-%m-%dT%H:%M:%S.%f%z') + timedelta(minutes=15)

        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        order_execute_time = f'{order.start_time:"%Y-%m-%dT%H:%M:%S.%f%z"}' if order.start_time is not None else 'now'
        message = f'Новая заявка!\n' \
                  f'Описание: {order.name}\n' \
                  f'Когда нужно выполнить заказ: {order_execute_time}\n' \
                  f'Предварительная цена: {order.price}\n' \
                  f'Коммисия сервиса: some 123\n' \
                  f'Стоимость без коммисии: some price\n' \
                  f'Ссылка для подтверждения: some link'

        count_of_messages_sent = 0
        for master_phone_number in masters_phone_numbers:
            _ = client.messages.create(
                to=master_phone_number,
                from_=settings.TWILIO_PHONE_NUMBER,
                body=message
            )
            count_of_messages_sent += 1
            if count_of_messages_sent == 3:
                send_notification_with_new_order_to_masters.apply_async(
                    eta=wait_time,
                    args=(
                        1,
                        masters_phone_numbers[count_of_messages_sent:],
                        wait_time
                    )
                )
                break


# TODO add link to message
# TODO add prefetch related(N+1) if necessary needed
@shared_task
def send_masters_info_to_customer(order_pk: int) -> None:
    """
    Send phone message with masters info to customer
    Args:
        order_pk: order pk
    """

    from api.order.models import Order

    order = Order.objects.get(pk=order_pk)
    masters = order.master.all()

    message = 'Мастер(а) найден(ы)\n' \
              'Информация о мастере(ах):\n'
    for master in masters:
        message += f'\tИмя мастера: {master.user.first_name} {master.user.last_name}\n' \
                   f'\tТелефон мастера: {master.user.phone_number}\n'

    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    _ = client.messages.create(
        to=order.customer.phone_number,
        from_=settings.TWILIO_PHONE_NUMBER,
        body=message
    )


@shared_task
def send_search_master_status_to_customer(data):
    """
    Send notification with status of masters search(if not enough masters accept order or etc)
    """

    print(1)

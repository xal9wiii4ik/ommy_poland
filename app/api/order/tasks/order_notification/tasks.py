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
        message = f'Новая заявка!\n' \
                  f'Описание: {order.name}\n' \
                  f'Когда нужно выполнить заказ: {order.start_time:"%Y-%m-%dT%H:%M:%S.%f%z"}\n' \
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

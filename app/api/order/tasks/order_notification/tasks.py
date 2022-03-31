import typing as tp

from twilio.rest import Client

from celery import shared_task

from ommy_polland import settings


# TODO update func description
@shared_task
def send_notification_with_new_order_to_masters(order_pk: int, masters_phone_numbers: tp.List[str]) -> None:
    """
    Send notification with new order to masters
    Args:
        order_pk: order pk
        masters_phone_numbers: masters phone numbers
    """

    from api.order.models import Order

    order = Order.objects.get(pk=order_pk)
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    # TODO update link
    message = f'Новая заявка!\n' \
              f'Описание: {order.name}\n' \
              f'Когда нужно выполнить заказ: {order.start_time:%Y-%m-%d %H-%M}\n' \
              f'Предварительная цена: {order.price}\n' \
              f'Комиссия сервиса: a lot of money\n' \
              f'Стоимость без комиссии: not enough money\n' \
              f'Link to confirm order: domain/some_link/order_pk/'
    for master_phone_number in masters_phone_numbers:
        # TODO add count; add sleep some time
        _ = client.messages.create(
            to=master_phone_number,
            from_=settings.TWILIO_PHONE_NUMBER,
            body=message
        )

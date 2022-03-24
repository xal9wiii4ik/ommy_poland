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

    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    # TODO update send message(mb link to site)
    for master_phone_number in masters_phone_numbers:
        _ = client.messages.create(
            to=master_phone_number,
            from_=settings.TWILIO_PHONE_NUMBER,
            body=f'You have new order, pk: {order_pk}'
        )

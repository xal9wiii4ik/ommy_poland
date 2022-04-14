import random

from twilio.rest import Client

from celery import shared_task

from ommy_polland import settings


# TODO add beat task for removing codes(mb if more than 1 day)
@shared_task
def send_phone_activate_message(user_pk: int) -> None:
    """
    Send activate message
    Args:
        user_pk: user pk
    """

    from api.authenticate.models import ActivateAccountCode
    from django.contrib.auth import get_user_model

    # create activate code
    user = get_user_model().objects.get(pk=user_pk)
    activate_code = ActivateAccountCode.objects.create(user=user, code=random.randint(1000, 9999))

    # send message to user
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    _ = client.messages.create(
        to=user.phone_number,
        from_=settings.TWILIO_PHONE_NUMBER,
        body=f'Ваш код подтверждения: {activate_code.code}'
    )

import random


from celery import shared_task

from api.utils.tasks_utils import send_phone_message


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

    send_phone_message(message=f'Ваш код подтверждения: {activate_code.code}', recipients_number=user.phone_number)


@shared_task
def resend_code(phone_number: str, code: int) -> None:
    """
    Resend activating code
    Args:
        phone_number: phone_number
        code: code
    """

    send_phone_message(message=f'Ваш код подтверждения: {code}', recipients_number=phone_number)

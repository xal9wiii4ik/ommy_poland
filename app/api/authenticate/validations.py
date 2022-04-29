from datetime import datetime

from django.utils import timezone

from rest_framework.serializers import ValidationError

wait_minutes = {0: 0, 1: 0.5, 2: 1, 3: 5, 4: 10, 5: 15, 6: 30, 7: 60}


def access_to_resend_code(last_resend_datetime: datetime, number_resending: int) -> None:
    """
    Check access to resend message with activating code
    Args:
        last_resend_datetime: current datetime
        number_resending: number of resending
    """

    if number_resending > 7:
        raise ValidationError(
            {'code': 'Вы израсходовали 7 попыток повторного отправки кода, обратитесь к администратору'}
        )

    now_datetime = timezone.now()
    delta = int((now_datetime - last_resend_datetime).seconds) / 60
    minutes = wait_minutes[number_resending]

    if delta < minutes:
        raise ValidationError(
            {'code': f'Вы еще не можете запросить повторную отправку кода, подождите {(minutes - delta) * 60} секунд'}
        )

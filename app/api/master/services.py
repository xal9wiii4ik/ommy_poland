import typing as tp

from django.contrib.auth import get_user_model

from api.authenticate.tasks.activate_user.tasks import send_phone_activate_message
from api.master.models import Master


def create_master_account(data: tp.Dict[str, tp.Any]):
    """
    Create master account
    Args:
        data: user data
    """

    # create user account
    del data['repeat_password']
    user = get_user_model().objects.create(
        username=data['username'],
        email=data['email'] if data.get('email') is not None else '',
        phone_number=data['phone_number'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        password=data['password'],
        is_active=False,
        is_master=True
    )
    del data['password']

    # create master
    Master.objects.create(
        user=user,
        work_experience=data['work_experience'],
        longitude=data['longitude'],
        latitude=data['latitude'],
        city=data['city'].lower()
    )
    send_phone_activate_message.delay(user.id)

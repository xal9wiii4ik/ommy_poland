import typing as tp

from django.contrib.auth import get_user_model

from api.authenticate.tasks.activate_user.tasks import send_phone_activate_message


def create_user_account(data: tp.Dict[str, tp.Any]):
    del data['repeat_password']
    user = get_user_model().objects.create(**data, is_active=False)
    del data['password']
    data['id'] = user.id

    send_phone_activate_message.delay(user.id)

import typing as tp

from django.contrib.auth import get_user_model

from api.authenticate.tasks.activate_user.tasks import send_phone_activate_message
from api.master.models import Master
from api.master.serializers import MasterExperienceModelSerializer


def create_master_account(
        data: tp.Dict[str, tp.Any],
        master_experiences: tp.List[tp.Dict[str, tp.Union[str, int]]]) -> int:
    """
    Create master account
    Args:
        data: user data
        master_experiences: list with dict with master work experiences and work spheres
    Return:
        user pk
    """

    # create user account
    del data['repeat_password']
    user = get_user_model().objects.create(
        email=data['email'] if data.get('email') is not None else '',
        phone_number=data['phone_number'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        password=data['password'],
        is_active=False,
        is_master=True,
        middle_name=data['middle_name'],
    )
    del data['password']

    # create master
    master = Master.objects.create(
        user=user,
        longitude=data['longitude'],
        latitude=data['latitude'],
        city=data['city'].lower(),
    )
    send_phone_activate_message.delay(user.id)
    if master_experiences is not None:
        for master_experience in master_experiences:
            serializer = MasterExperienceModelSerializer(data=master_experience)
            if serializer.is_valid():
                serializer.validated_data['master'] = master
                serializer.save()
    return user.pk

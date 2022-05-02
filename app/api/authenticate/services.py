import typing as tp

from api.authenticate.models import ActivateAccountCode


def activate_account(data: tp.Dict[str, tp.Any]) -> tp.Union[str, bool]:
    """
    Activate user account
    Args:
        data: dict with data
    Return:
        username if activate code exist else False
    """

    activate_code = ActivateAccountCode.objects.get(code=data['code'], user__pk=data['user_pk'])
    user = activate_code.user
    user.is_active = True
    user.save()
    activate_code.delete()
    return user.phone_number

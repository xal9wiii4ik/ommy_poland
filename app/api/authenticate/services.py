import typing as tp

from django.core.exceptions import ObjectDoesNotExist

from api.authenticate.models import ActivateAccountCode


def activate_account(data: tp.Dict[str, tp.Any]) -> bool:
    """
    Activate user account
    Args:
        data: dict with data
    Return:
        True if activate code exist else False
    """

    try:
        activate_code = ActivateAccountCode.objects.get(code=data['code'], user__pk=data['user_pk'])
    except ObjectDoesNotExist:
        return False
    else:
        # update user field
        user = activate_code.user
        user.is_active = True
        user.save()
        # remove activate code
        activate_code.delete()
        return True

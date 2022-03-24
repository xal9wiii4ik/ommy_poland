from django.contrib.auth import get_user_model
from django.db import models


class ActivateAccountCode(models.Model):
    """
    Model which contain user account and codes for activating this accounts
    """

    user = models.ForeignKey(to=get_user_model(),
                             related_name='activate_code_user',
                             on_delete=models.CASCADE,
                             verbose_name='activate code for user')
    code = models.BigIntegerField(verbose_name='activate code')
    created_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'pk: {self.pk}, user: {self.user.pk}'

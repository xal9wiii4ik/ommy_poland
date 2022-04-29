from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


class ActivateAccountCode(models.Model):
    """
    Model which contain user account and codes for activating this accounts
    """

    class Meta:
        verbose_name = 'Activate Account Code'

    user = models.ForeignKey(to=get_user_model(),
                             related_name='activate_code_user',
                             on_delete=models.CASCADE,
                             verbose_name='activate code for user')
    code = models.BigIntegerField(verbose_name='activate code')
    created_datetime = models.DateTimeField(auto_now_add=True)
    last_resend_datetime = models.DateTimeField(verbose_name='Last resend code datetime',
                                                default=timezone.now,
                                                null=True,
                                                blank=True)
    number_resending = models.PositiveIntegerField(verbose_name='Number of resending code',
                                                   default=0,
                                                   null=True,
                                                   blank=True)

    def __str__(self) -> str:
        return f'pk: {self.pk}, user: {self.user.pk}'

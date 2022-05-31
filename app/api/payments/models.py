from django.db import models

from api.master.models import Master
from api.order.models import Order
from api.order.models_validators import validate_positive_number


class Commission(models.Model):
    """ Model for table commission """

    master = models.ManyToManyField(
        to=Master,
        related_name='master_commission',
        verbose_name='Master'
    )
    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        related_name='order_commission',
        verbose_name='Order'
    )
    amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Commission amount',
        validators=[validate_positive_number],
        null=True
    )
    closing_order_datetime = models.DateTimeField(null=True, blank=True, verbose_name='Closing order date')

    def __str__(self) -> str:
        return f'pk: {self.pk}, order_pk: {self.order.pk}, amount: {self.amount}'


from django.contrib import admin
from django.utils.safestring import mark_safe

from api.payments.models import Commission


@admin.register(Commission)
class CommissionModelAdmin(admin.ModelAdmin):
    """ Display model Commission in admin panel """

    @staticmethod
    def master_id(obj: Commission):
        message = ''
        for experience in obj.master.all():
            message += f'<div>{experience.id}</div><p>'
        return mark_safe(message)

    @staticmethod
    def order_id(obj: Commission) -> str:
        return obj.order.id

    list_display = ('id', 'master_id', 'order_id', 'amount', 'closing_order_datetime',)
    list_filter = ('master__id', 'closing_order_datetime',)

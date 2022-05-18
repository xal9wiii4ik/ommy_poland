import typing as tp

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.master.models import Master
from api.order.models import Order


class CommissionSerializer(serializers.Serializer):
    """ Serializer for creating commission """

    masters_pks = serializers.ListField(child=serializers.IntegerField(min_value=1))
    missing_pks = serializers.ListField(child=serializers.IntegerField(min_value=1), read_only=True)
    order_pk = serializers.IntegerField(min_value=1)

    @staticmethod
    def validate_order_pk(order_pk):
        is_exist = Order.objects.filter(pk=order_pk)
        if not is_exist:
            raise ValidationError('order with given pk does not exist')
        return order_pk

    # TODO test O time
    def validate(self, attrs: tp.Dict[str, tp.Any]):
        pks = [master.pk for master in Master.objects.filter(pk__in=attrs['masters_pks'])]
        attrs['missing_pks'] = set(attrs['masters_pks']).difference(pks)
        attrs['masters_pks'] = set(attrs['masters_pks']).intersection(pks)
        if not attrs['masters_pks']:
            raise ValidationError({'masters_pks': 'pks were not found in our database'})
        return attrs

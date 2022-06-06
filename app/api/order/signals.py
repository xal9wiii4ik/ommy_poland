import typing as tp

from api.order.models import Order, OrderStatus
from api.payments.models import Commission


def remove_stores_from_user_managed_groups(instance: Order,
                                           action: str,
                                           pk_set: tp.Set[int],
                                           **kwargs: tp.Any) -> None:
    """
    Updating amount and masters of the commission or creating commission for order
    Args:
        instance: current Order instance
        action: current action
        pk_set: set with master pks
    """

    from api.payments.models import Commission

    if action == 'post_add' and instance.status == OrderStatus.DONE.name:
        commission, created = Commission.objects.get_or_create(order=instance)
        count_masters = len(pk_set) if created else instance.master.all().count()
        commission.amount = (instance.price / count_masters) * 20 / 100
        commission.master.add(*pk_set)
        commission.save()
    if action == 'post_remove' and instance.status == OrderStatus.DONE.name:
        commission = Commission.objects.get(order=instance)
        count_masters = instance.master.all().count()
        commission.amount = 0 if not count_masters else (instance.price / count_masters) * 20 / 100
        commission.master.remove(*pk_set)
        commission.save()


def creating_commission(sender: Order, instance: Order, created: bool, **kwargs: tp.Any) -> None:
    """
    Creating new commission for order if order move to status done
    Args:
        sender: Order
        instance: Order
        created: is created
    """

    if instance.status == OrderStatus.DONE.name:
        commission, is_created = Commission.objects.get_or_create(order=instance)
        if is_created:
            pk_set = [master.pk for master in instance.master.all()]
            commission.amount = 0 if not pk_set else (instance.price / len(pk_set)) * 20 / 100
            commission.master.add(*pk_set)
            commission.save()

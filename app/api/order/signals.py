import typing as tp

from api.order.models import Order


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

    # TODO add tests
    if action == 'post_add':
        commission, created = Commission.objects.get_or_create(order=instance)
        count_masters = len(pk_set) if created else instance.master.all().count()
        commission.amount = (instance.price / count_masters) * 20 / 100
        commission.master.add(*pk_set)
        commission.save()
    if action == 'post_remove':
        commission = Commission.objects.get(order=instance)
        commission.master.remove(*pk_set)

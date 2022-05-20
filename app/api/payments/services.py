import typing as tp


from api.order.models import Order
from api.payments.models import Commission


def create_commission(data: tp.Dict[str, tp.Any]):
    """
    Creating commission
    Args:
        data: Dict with request data
    """

    order = Order.objects.get(pk=data['order_pk'])
    masters_pks = data['masters_pks']
    amount = (order.price / len(masters_pks)) * 20 / 100
    commision = Commission.objects.create(
        order=order,
        amount=amount
    )

    for pk in masters_pks:
        commision.master.add(pk)

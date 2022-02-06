import typing as tp
import logging

from apps.order.models import Order, OrderFile


def create_order_files(order_id: int, files: tp.List[tp.IO]) -> None:
    """ Func for saving pictures in database
    Args:
        order_id: post id
        files: list with files
    """

    order = Order.objects.get(pk=order_id)
    for file in files:
        try:
            OrderFile.objects.create(order=order, file=file)
        except Exception:
            logging.exception(msg=f'Something was wrong with creating PostImage for post {order_id}')

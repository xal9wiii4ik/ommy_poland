import typing as tp

from celery import shared_task


# TODO update func description
@shared_task
def send_notification_with_new_order_to_masters(order_pk: int, masters_queue: tp.List[str]) -> None:
    """
    Send notification with new order to masters
    """

    for master in masters_queue:
        # print(order)
        print(master)

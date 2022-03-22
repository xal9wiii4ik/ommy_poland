import typing as tp

from django.db.models import Model


def send_files_for_notifications(order: Model, chat_id: tp.Any) -> None:
    """
    Sending files to chats
    Args:
        order: current order
        chat_id: chat_id
    """

    from apps.order.models import OrderFile
    from apps.telegram_bot.loader import dp

    order_files = OrderFile.objects.filter(order=order)

    for order_file in order_files:
        dp.loop.run_until_complete(
            dp.bot.send_message(chat_id=chat_id, text=order_file.bucket_path)
        )

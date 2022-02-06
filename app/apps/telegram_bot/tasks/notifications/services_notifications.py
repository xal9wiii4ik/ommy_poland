
from django.db.models import Model


def send_files_for_notifications(order: Model, chat_id: int) -> None:
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
        if order_file.file_type == 'video':
            dp.loop.run_until_complete(
                dp.bot.send_video(chat_id=chat_id, video=order_file.file.read())
            )
        elif order_file.file_type == 'audio':
            dp.loop.run_until_complete(
                dp.bot.send_voice(chat_id=chat_id, voice=order_file.file.read())
            )
        else:
            dp.loop.run_until_complete(
                dp.bot.send_photo(chat_id=chat_id, photo=order_file.file.read())
            )
        order_file.file.seek(0)

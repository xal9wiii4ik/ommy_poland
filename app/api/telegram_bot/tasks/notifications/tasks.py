import logging

from celery import shared_task

from api.telegram_bot.tasks.notifications.services_notifications import send_files_for_notifications
from ommy_polland import settings


@shared_task
def send_notification_with_new_order_to_order_chat(order_pk: int) -> None:
    """
    Send notification with new order to order chat
    Args:
        order_pk: current order pk
    """

    from django.db.models import F
    from api.order.models import Order
    from api.telegram_bot.loader import dp
    from api.order.serializers import GoogleSheetOrderSerializer

    logging.info(f'Start send notification to ommy chat with new order: {order_pk}')

    order = Order.objects.select_related('customer').select_related('work_sphere').annotate(
        phone_number=F('customer__phone_number'),
        work_sphere_name=F('work_sphere__name'),
        first_name=F('customer__first_name'),
    ).get(pk=order_pk)
    serializer = GoogleSheetOrderSerializer(order)
    serializer_data = serializer.data

    message = f'New order with pk: {order.pk} has been created\n' \
              f'========Order info========\n' \
              f'Work_sphere: {serializer_data["work_sphere_name"]}\n' \
              f'Order name: {order.name}\n' \
              f'Work duration: {order.number_employees}\n' \
              f'Desired time end work: {order.desired_time_end_work}\n' \
              f'Start work time: {serializer_data["start_time"]}\n' \
              f'Price: {order.price} BYN\n' \
              f'Description: {order.description}\n' \
              f'Address: {order.address}\n' \
              f'========Customer info========\n' \
              f'Phone number: {order.customer.phone_number}\n' \
              f'First name: {order.customer.first_name}\n'
    dp.loop.run_until_complete(dp.bot.send_message(chat_id=settings.ORDER_CHAT_ID, text=message))

    send_files_for_notifications(order=order, chat_id=settings.ORDER_CHAT_ID)

    logging.info(f'Notification to ommy chat with new order: {order_pk} was sent')


@shared_task
def send_cancel_order_to_order_chat(order_pk: int) -> None:
    """
    Send notification to order chat with cancel order
    Args:
        order_pk: order pk
    """

    from api.telegram_bot.loader import dp

    message = f'Order with id: {order_pk} was closed'
    dp.loop.run_until_complete(dp.bot.send_message(chat_id=settings.ORDER_CHAT_ID, text=message))


@shared_task
def notification_with_coming_order(order_pk: int) -> None:
    """
    Send notification with coming order
    Args:
        order_pk: order pk
    """

    from api.order.models import Order
    from api.telegram_bot.loader import dp

    logging.info(f'Send notifications to ommy chat with coming order to ommy chat {order_pk}')

    order = Order.objects.get(pk=order_pk)
    message = f'Coming order: {order_pk}\n' \
              f'Start work time: {order.start_time}\n' \
              f'Number Employees: {order.number_employees}\n' \
              f'Phone number: {order.customer.phone_number}\n' \
              f'First name: {order.customer.first_name}\n' \
              f'Last name: {order.customer.last_name}\n'
    dp.loop.run_until_complete(dp.bot.send_message(chat_id=settings.ORDER_CHAT_ID, text=message))

    logging.info(f'Notification to ommy chat with coming order: {order_pk} was sent')


# @shared_task
# def send_notification_with_new_order_to_masters_chats(order_pk: int) -> None:
#     """
#     Send notification with new order to masters chats
#     Args:
#         order_pk: current order pk
#     """
#
#     from apps.telegram_bot.inline_keyboards import generate_execution_order_markup
#     from apps.order.models import Order
#     from apps.telegram_bot.loader import dp
#     from apps.account.models import Master
#
#     logging.info(f'Start send notification to masters chats with new order: {order_pk}')
#
#     order = Order.objects.get(pk=order_pk)
#
#     masters = Master.objects.filter(is_notified=True)
#
#     additional_message = 'Появился новый заказ:\n'
#
#     if not order.work_sphere.under_consideration:
#         if any(masters.filter(work_sphere=order.work_sphere)):
#             masters = masters.filter(work_sphere=order.work_sphere)
#         else:
#             additional_message = f'У нас появился заказ на профиль {order.work_sphere.name}. \n' \
#                                  f'На данный момент у нас нету мастера по этой специальности. \n' \
#                                  f'Если вы желаете можете взяться за заказ\n'
#     else:
#         additional_message = 'Заказчик указал новую категорию, которая сейчас находится в обработке, ' \
#                              'но если вам будет интересно, то вы можете принять заказ уже сейчас.\n'
#
#     masters_for_order_ids = [master.telegram_chat_id for master in masters]
#
#     message = f'{additional_message}\n' \
#               f'Имя заказа: {order.name}\n' \
#               f'Описание заказа: {order.description}\n' \
#               f'Если вы готовы взять заказ, нажмите кнопку взять заказ. \n' \
#               f'Желательная цена для клиента от: {order.price_from}р до: {order.price_to}\n' \
#               f'Позже мы вам пришлем подробности заказа\n' \
#               f'Если вы не возьмете заказ это никак не повлияет на ваш рейтинг, заказ перейдет другому мастеру.'
#
#     for masters_chat_id in masters_for_order_ids:
#         reply_markup = dp.loop.run_until_complete(generate_execution_order_markup(order_pk=order_pk))
#         try:
#             dp.loop.run_until_complete(
#                 dp.bot.send_message(chat_id=masters_chat_id, text=message, reply_markup=reply_markup)
#             )
#             send_files_for_notifications(order=order, chat_id=masters_chat_id)
#         except Exception:
#             send_notification_to_deploy_chat.delay(
#                 'errors',
#                 f'Something was wrong with send_notification_with_new_order_to_masters_chats; order_pk: {order.pk}\n'
#                 f'{traceback.format_exc()}')
#             logging.info(f'Chat not fount {masters_chat_id}')
#
#     logging.info(f'Notification to masters chats with new order: {order_pk} was sent')
#
#
# @shared_task
# def send_notification_with_new_work_sphere(work_sphere_id: int, work_sphere_name: str) -> None:
#     """
#     Send notification with new work sphere
#     Args:
#         work_sphere_id: id of work sphere
#         work_sphere_name: work sphere name
#     """
#
#     from apps.telegram_bot.loader import dp
#
#     logging.info(f'Start send notification with new work sphere; name: {work_sphere_name}, id: {work_sphere_id}')
#
#     message = f'Master add new work sphere \n' \
#               f'Work sphere id: {work_sphere_id} \n' \
#               f'Work sphere name: {work_sphere_name}\n' \
#               f'Go to admin and consider this area (or under_consideration set true or delete this sphere)'
#     dp.loop.run_until_complete(dp.bot.send_message(chat_id=settings.OMMY_ORDER_CHAT_ID, text=message))
#
#     logging.info(f'Notification with new work sphere was sent; name: {work_sphere_name}, id: {work_sphere_id}')
#
#
# @shared_task
# def send_notification_to_deploy_chat(message_type: str, message: str) -> None:
#     """
#     Send notification with success or error message to deploy chat
#     Args:
#         message_type: message type(error or success)
#         message: message
#     """
#
#     from apps.telegram_bot.loader import dp
#
#     chat_id = settings.ERROR_CHAT if message_type == 'errors' else settings.SUCCESS_CHAT
#
#     text = f'ERROR MESSAGE:\n' if message_type == 'errors' else 'SUCCESS MESSAGE:\n'
#     text += message
#
#     dp.loop.run_until_complete(dp.bot.send_message(chat_id=chat_id, text=text))
